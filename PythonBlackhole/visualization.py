"""
Visualization Module
Handles rendering of the black hole simulation in the terminal
"""

import os
import sys
import math
from config import *
from utils import *


class Renderer:
    """Handles terminal rendering of the simulation"""
    
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.zoom = ZOOM_LEVEL
        self.view_range = VIEW_RANGE
        
        # Screen buffer
        self.buffer = [[' ' for _ in range(width)] for _ in range(height)]
        self.color_buffer = [[COLOR_RESET for _ in range(width)] for _ in range(height)]
        
        # View mode
        self.view_mode = 'top'  # 'top', 'side', '3d'
        self.rotation_angle = 0.0
        
        # Display options
        self.show_grid = False
        self.show_zones = True
        self.show_trails = True
        self.show_accretion_disk = True
        self.show_info = True
        
    def clear_screen(self):
        """Clear the terminal screen"""
        if os.name == 'nt':
            os.system('cls')
        else:
            print('\033[2J\033[H', end='')
    
    def clear_buffer(self):
        """Clear the rendering buffer"""
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.color_buffer = [[COLOR_RESET for _ in range(self.width)] for _ in range(self.height)]
    
    def world_to_screen(self, position):
        """
        Convert world coordinates to screen coordinates
        Returns (x, y) or None if out of bounds
        """
        if self.view_mode == 'top':
            # Top-down view (X-Y plane)
            world_x = position.x / (self.view_range * self.zoom)
            world_y = position.y / (self.view_range * self.zoom)
        elif self.view_mode == 'side':
            # Side view (X-Z plane)
            world_x = position.x / (self.view_range * self.zoom)
            world_y = position.z / (self.view_range * self.zoom)
        else:  # 3d view
            # Simple 3D projection
            rotated_x = position.x * math.cos(self.rotation_angle) - position.y * math.sin(self.rotation_angle)
            rotated_y = position.x * math.sin(self.rotation_angle) + position.y * math.cos(self.rotation_angle)
            world_x = rotated_x / (self.view_range * self.zoom)
            world_y = (rotated_y + position.z * 0.5) / (self.view_range * self.zoom)
        
        # Convert to screen coordinates
        screen_x = int(self.center_x + world_x * self.center_x)
        screen_y = int(self.center_y - world_y * self.center_y)  # Flip Y axis
        
        # Check bounds
        if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
            return (screen_x, screen_y)
        return None
    
    def draw_pixel(self, x, y, char, color=COLOR_RESET):
        """Draw a character at screen coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = char
            self.color_buffer[y][x] = color
    
    def draw_circle(self, center_pos, radius, char, color=COLOR_RESET, filled=False):
        """Draw a circle in world coordinates"""
        # Sample points around the circle
        num_points = max(20, int(radius * 2))
        
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            
            if self.view_mode == 'top':
                x = center_pos.x + radius * math.cos(angle)
                y = center_pos.y + radius * math.sin(angle)
                z = center_pos.z
            elif self.view_mode == 'side':
                x = center_pos.x + radius * math.cos(angle)
                y = center_pos.y
                z = center_pos.z + radius * math.sin(angle)
            else:  # 3d
                x = center_pos.x + radius * math.cos(angle)
                y = center_pos.y + radius * math.sin(angle)
                z = center_pos.z
            
            pos = Vector3D(x, y, z)
            screen_pos = self.world_to_screen(pos)
            
            if screen_pos:
                self.draw_pixel(screen_pos[0], screen_pos[1], char, color)
    
    def draw_line(self, pos1, pos2, char, color=COLOR_RESET):
        """Draw a line between two world positions"""
        screen_pos1 = self.world_to_screen(pos1)
        screen_pos2 = self.world_to_screen(pos2)
        
        if not screen_pos1 or not screen_pos2:
            return
        
        # Bresenham's line algorithm
        x1, y1 = screen_pos1
        x2, y2 = screen_pos2
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            self.draw_pixel(x1, y1, char, color)
            
            if x1 == x2 and y1 == y2:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    
    def render_black_hole(self, black_hole):
        """Render the black hole and its zones"""
        rs = black_hole.schwarzschild_radius
        
        # Draw zones if enabled
        if self.show_zones:
            # Event horizon
            self.draw_circle(
                black_hole.position,
                EVENT_HORIZON_RADIUS * rs,
                '█',
                COLOR_EVENT_HORIZON
            )
            
            # Photon sphere
            self.draw_circle(
                black_hole.position,
                PHOTON_SPHERE_RADIUS * rs,
                '○',
                COLOR_PHOTON_SPHERE
            )
            
            # ISCO
            self.draw_circle(
                black_hole.position,
                ISCO_RADIUS * rs,
                '·',
                COLOR_WARNING
            )
        
        # Draw black hole center
        center_screen = self.world_to_screen(black_hole.position)
        if center_screen:
            self.draw_pixel(center_screen[0], center_screen[1], CHAR_BLACK_HOLE, COLOR_BLACK_HOLE)
    
    def render_accretion_disk(self, accretion_disk):
        """Render the accretion disk"""
        if not self.show_accretion_disk:
            return
        
        for particle in accretion_disk.get_particles_in_view():
            screen_pos = self.world_to_screen(particle['position'])
            if screen_pos:
                color = get_color_from_temperature(particle['temperature'])
                self.draw_pixel(screen_pos[0], screen_pos[1], CHAR_ACCRETION, color)
    
    def render_particles(self, particle_system):
        """Render all particles"""
        for particle in particle_system.get_active_particles():
            # Draw trail if enabled
            if self.show_trails and len(particle.trail) > 1:
                for i in range(len(particle.trail) - 1):
                    self.draw_line(
                        particle.trail[i],
                        particle.trail[i + 1],
                        CHAR_PARTICLE_TRAIL,
                        particle.color
                    )
            
            # Draw particle
            screen_pos = self.world_to_screen(particle.position)
            if screen_pos:
                self.draw_pixel(screen_pos[0], screen_pos[1], particle.char, particle.color)
    
    def render_grid(self):
        """Render coordinate grid"""
        if not self.show_grid:
            return
        
        # Draw grid lines
        grid_spacing = 10
        for i in range(-50, 51, grid_spacing):
            # Vertical lines
            pos1 = Vector3D(i, -50, 0)
            pos2 = Vector3D(i, 50, 0)
            self.draw_line(pos1, pos2, CHAR_GRID, '\033[90m')
            
            # Horizontal lines
            pos1 = Vector3D(-50, i, 0)
            pos2 = Vector3D(50, i, 0)
            self.draw_line(pos1, pos2, CHAR_GRID, '\033[90m')
    
    def render_info_panel(self, black_hole, particle_system, simulation_time, fps):
        """Render information panel"""
        if not self.show_info:
            return
        
        info_lines = []
        
        # Title
        info_lines.append(f"{COLOR_INFO}╔═══ BLACK HOLE SIMULATION ═══╗{COLOR_RESET}")
        
        # Black hole info
        info_lines.append(f"{COLOR_INFO}Black Hole:{COLOR_RESET}")
        info_lines.append(f"  Mass: {format_mass(black_hole.mass)}")
        info_lines.append(f"  Rs: {format_distance(black_hole.schwarzschild_radius)}")
        info_lines.append(f"  Temp: {format_temperature(black_hole.temperature)}")
        
        # Particle statistics
        stats = particle_system.get_statistics()
        info_lines.append(f"{COLOR_INFO}Particles:{COLOR_RESET}")
        info_lines.append(f"  Active: {stats['active']}/{MAX_PARTICLES}")
        info_lines.append(f"  Created: {stats['total_created']}")
        info_lines.append(f"  Captured: {stats['captured']}")
        info_lines.append(f"  Escaped: {stats['escaped']}")
        
        # Simulation info
        info_lines.append(f"{COLOR_INFO}Simulation:{COLOR_RESET}")
        info_lines.append(f"  Time: {simulation_time:.2f} s")
        info_lines.append(f"  FPS: {fps:.1f}")
        info_lines.append(f"  View: {self.view_mode.upper()}")
        info_lines.append(f"  Zoom: {self.zoom:.2f}x")
        
        # Controls
        info_lines.append(f"{COLOR_INFO}Controls:{COLOR_RESET}")
        info_lines.append(f"  SPACE: Add particle")
        info_lines.append(f"  V: Change view")
        info_lines.append(f"  +/-: Zoom")
        info_lines.append(f"  G: Toggle grid")
        info_lines.append(f"  T: Toggle trails")
        info_lines.append(f"  A: Toggle accretion")
        info_lines.append(f"  C: Clear particles")
        info_lines.append(f"  Q: Quit")
        
        # Draw info panel on the right side
        start_x = self.width - 35
        for i, line in enumerate(info_lines):
            if i < self.height:
                # Draw directly to avoid buffer conflicts
                pass  # Will be drawn in display method
        
        return info_lines
    
    def display(self, info_lines=None):
        """Display the buffer to the terminal"""
        output = []
        
        # Build output string
        for y in range(self.height):
            line = ""
            current_color = COLOR_RESET
            
            for x in range(self.width):
                char = self.buffer[y][x]
                color = self.color_buffer[y][x]
                
                # Only change color if different
                if color != current_color:
                    line += color
                    current_color = color
                
                line += char
            
            line += COLOR_RESET
            output.append(line)
        
        # Overlay info panel
        if info_lines:
            start_x = self.width - 35
            for i, info_line in enumerate(info_lines):
                if i < len(output):
                    # Replace part of the line with info
                    line = output[i]
                    if len(line) > start_x:
                        output[i] = line[:start_x] + info_line
        
        # Clear screen and print
        self.clear_screen()
        print('\n'.join(output), flush=True)
    
    def toggle_view_mode(self):
        """Cycle through view modes"""
        modes = ['top', 'side', '3d']
        current_index = modes.index(self.view_mode)
        self.view_mode = modes[(current_index + 1) % len(modes)]
    
    def zoom_in(self):
        """Increase zoom level"""
        self.zoom = min(self.zoom * 1.2, 10.0)
    
    def zoom_out(self):
        """Decrease zoom level"""
        self.zoom = max(self.zoom / 1.2, 0.1)
    
    def toggle_grid(self):
        """Toggle grid display"""
        self.show_grid = not self.show_grid
    
    def toggle_trails(self):
        """Toggle particle trails"""
        self.show_trails = not self.show_trails
    
    def toggle_accretion_disk(self):
        """Toggle accretion disk display"""
        self.show_accretion_disk = not self.show_accretion_disk
    
    def rotate_view(self, angle_delta):
        """Rotate 3D view"""
        self.rotation_angle += angle_delta
