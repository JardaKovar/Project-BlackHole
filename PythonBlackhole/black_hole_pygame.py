"""
Fast 3D Black Hole Simulation using Pygame
Smooth graphics with mouse controls
"""

import pygame
import numpy as np
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Physics constants
G = 6.67430e-11
C = 299792458
SOLAR_MASS = 1.989e30
BLACK_HOLE_MASS = 10 * SOLAR_MASS
SCHWARZSCHILD_RADIUS = (2 * G * BLACK_HOLE_MASS) / (C ** 2)

# Simulation scale
SCALE = 1.0

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
DARK_RED = (139, 0, 0)
PURPLE = (138, 43, 226)


class Camera:
    """3D Camera for viewing the black hole"""
    
    def __init__(self):
        self.distance = 150
        self.angle_x = 0
        self.angle_y = 0
        self.dragging = False
        self.last_mouse_pos = None
        
    def rotate(self, dx, dy):
        """Rotate camera"""
        self.angle_y += dx * 0.005
        self.angle_x += dy * 0.005
        self.angle_x = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.angle_x))
    
    def zoom(self, amount):
        """Zoom in/out"""
        self.distance *= (0.9 if amount > 0 else 1.1)
        self.distance = max(50, min(300, self.distance))
    
    def project(self, x, y, z):
        """Project 3D point to 2D screen"""
        # Rotate around Y axis
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        # Rotate around X axis
        cos_x = math.cos(self.angle_x)
        sin_x = math.sin(self.angle_x)
        y_rot = y * cos_x - z_rot * sin_x
        z_final = y * sin_x + z_rot * cos_x
        
        # Apply camera distance
        z_final += self.distance
        
        # Perspective projection
        if z_final <= 0:
            return None
        
        scale = 500 / z_final
        screen_x = int(WIDTH / 2 + x_rot * scale)
        screen_y = int(HEIGHT / 2 - y_rot * scale)
        
        return (screen_x, screen_y, z_final)


class Particle:
    """Particle affected by black hole gravity"""
    
    def __init__(self, x, y, z, vx, vy, vz):
        self.pos = np.array([x, y, z], dtype=float)
        self.vel = np.array([vx, vy, vz], dtype=float)
        self.trail = []
        self.alive = True
        self.color = GREEN
        
    def update(self, dt):
        """Update particle physics"""
        if not self.alive:
            return
        
        # Distance from black hole
        r = np.linalg.norm(self.pos)
        
        # Check if captured
        if r < 5:  # Event horizon
            self.alive = False
            return
        
        # Gravitational acceleration
        if r > 0:
            accel = -100.0 * self.pos / (r ** 2)
            
            # Update velocity and position
            self.vel += accel * dt
            self.pos += self.vel * dt
            
            # Store trail
            self.trail.append(self.pos.copy())
            if len(self.trail) > 30:
                self.trail.pop(0)
            
            # Update color based on speed
            speed = np.linalg.norm(self.vel)
            if speed > 20:
                self.color = RED
            elif speed > 10:
                self.color = ORANGE
            else:
                self.color = GREEN


class BlackHoleSimulation:
    """Main simulation class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("3D Black Hole Simulation - Interactive")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        self.camera = Camera()
        self.particles = []
        self.running = True
        self.paused = False
        
        # Add initial particles
        self.add_random_particles(8)
        
    def add_random_particles(self, count):
        """Add random particles"""
        for _ in range(count):
            angle = np.random.uniform(0, 2 * math.pi)
            radius = np.random.uniform(40, 80)
            height = np.random.uniform(-20, 20)
            
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            y = height
            
            # Orbital velocity
            v_orbital = math.sqrt(100.0 / radius) * 0.8
            vx = -v_orbital * math.sin(angle)
            vz = v_orbital * math.cos(angle)
            vy = 0
            
            self.particles.append(Particle(x, y, z, vx, vy, vz))
    
    def draw_sphere(self, center_3d, radius, color, segments=30):
        """Draw a 3D sphere with shading"""
        points_2d = []
        
        for i in range(segments):
            lat = (i / segments) * math.pi
            for j in range(segments * 2):
                lon = (j / (segments * 2)) * 2 * math.pi
                
                x = center_3d[0] + radius * math.sin(lat) * math.cos(lon)
                y = center_3d[1] + radius * math.cos(lat)
                z = center_3d[2] + radius * math.sin(lat) * math.sin(lon)
                
                proj = self.camera.project(x, y, z)
                if proj:
                    # Calculate lighting (simple)
                    light_dir = np.array([1, 1, 1])
                    normal = np.array([x - center_3d[0], y - center_3d[1], z - center_3d[2]])
                    if np.linalg.norm(normal) > 0:
                        normal = normal / np.linalg.norm(normal)
                        brightness = max(0, np.dot(normal, light_dir / np.linalg.norm(light_dir)))
                    else:
                        brightness = 0
                    
                    points_2d.append((proj[0], proj[1], proj[2], brightness))
        
        # Sort by depth and draw
        points_2d.sort(key=lambda p: -p[2])
        for px, py, _, brightness in points_2d:
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                # Apply brightness to color
                shaded_color = tuple(int(c * brightness) for c in color)
                pygame.draw.circle(self.screen, shaded_color, (px, py), 3)
    
    def draw_circle_3d(self, center_3d, radius, color, segments=50):
        """Draw a 3D circle"""
        points = []
        for i in range(segments + 1):
            angle = (i / segments) * 2 * math.pi
            x = center_3d[0] + radius * math.cos(angle)
            z = center_3d[2] + radius * math.sin(angle)
            y = center_3d[1]
            
            proj = self.camera.project(x, y, z)
            if proj:
                points.append((proj[0], proj[1]))
        
        if len(points) > 2:
            pygame.draw.lines(self.screen, color, False, points, 2)
    
    def draw_accretion_disk(self):
        """Draw accretion disk with particles - optimized"""
        rotation_offset = pygame.time.get_ticks() * 0.0002
        
        # Draw disk as particles for better 3D effect and performance
        for ring_radius in range(10, 40, 3):
            segments = 30  # Reduced for performance
            
            for i in range(segments):
                angle = (i / segments) * 2 * math.pi + rotation_offset
                
                # Position in disk
                x = ring_radius * math.cos(angle)
                z = ring_radius * math.sin(angle)
                y = np.random.normal(0, 0.2)  # Thin disk
                
                proj = self.camera.project(x, y, z)
                if proj and 0 <= proj[0] < WIDTH and 0 <= proj[1] < HEIGHT:
                    # Color based on radius (hot inner, cool outer)
                    temp_factor = 1.0 - (ring_radius - 10) / 30
                    
                    if temp_factor > 0.7:  # Very hot - white/yellow
                        color = (255, 255, int(200 * temp_factor))
                    elif temp_factor > 0.4:  # Hot - orange
                        color = (255, int(165 * temp_factor), 0)
                    else:  # Cooler - red
                        color = (int(255 * temp_factor), int(50 * temp_factor), 0)
                    
                    # Size based on distance
                    size = max(1, int(3 - proj[2] / 100))
                    pygame.draw.circle(self.screen, color, (proj[0], proj[1]), size)
    
    def draw(self):
        """Draw everything - optimized"""
        self.screen.fill(BLACK)
        
        # Draw accretion disk (behind black hole)
        self.draw_accretion_disk()
        
        # Draw photon sphere (single layer for performance)
        self.draw_circle_3d([0, 0, 0], 7.5, YELLOW, segments=40)
        
        # Draw event horizon glow (reduced layers)
        for glow in range(2, 0, -1):
            glow_color = (255, 100 + glow * 50, 0)
            self.draw_circle_3d([0, 0, 0], 5 + glow * 0.5, glow_color, segments=40)
        
        # Draw 3D black hole sphere
        self.draw_sphere([0, 0, 0], 5, (20, 0, 0), segments=20)
        
        # Draw center with glow
        center_proj = self.camera.project(0, 0, 0)
        if center_proj:
            radius = int(500 / center_proj[2] * 5)
            if radius > 0:
                # Filled black center
                pygame.draw.circle(self.screen, BLACK, (center_proj[0], center_proj[1]), radius)
                # Red edge glow (reduced layers)
                for i in range(3, 0, -1):
                    edge_color = (200 - i * 40, 0, 0)
                    pygame.draw.circle(self.screen, edge_color, (center_proj[0], center_proj[1]), radius + i, 1)
        
        # Draw particles and trails
        for particle in self.particles:
            if not particle.alive:
                continue
            
            # Draw trail
            if len(particle.trail) > 1:
                trail_points = []
                for pos in particle.trail:
                    proj = self.camera.project(pos[0], pos[1], pos[2])
                    if proj:
                        trail_points.append((proj[0], proj[1]))
                
                if len(trail_points) > 1:
                    pygame.draw.lines(self.screen, CYAN, False, trail_points, 1)
            
            # Draw particle
            proj = self.camera.project(particle.pos[0], particle.pos[1], particle.pos[2])
            if proj:
                pygame.draw.circle(self.screen, particle.color, (proj[0], proj[1]), 4)
                pygame.draw.circle(self.screen, WHITE, (proj[0], proj[1]), 4, 1)
        
        # Draw info
        self.draw_info()
        
        pygame.display.flip()
    
    def draw_info(self):
        """Draw information panel"""
        info_lines = [
            "3D BLACK HOLE SIMULATION",
            "",
            f"Particles: {len([p for p in self.particles if p.alive])}",
            f"FPS: {int(self.clock.get_fps())}",
            "",
            "CONTROLS:",
            "Left-click + Drag: Rotate",
            "Scroll: Zoom",
            "Right-click: Add particle",
            "SPACE: Pause/Resume",
            "R: Reset",
            "ESC: Quit",
        ]
        
        y = 10
        for line in info_lines:
            if line == "3D BLACK HOLE SIMULATION":
                text = self.font.render(line, True, YELLOW)
            elif line == "CONTROLS:":
                text = self.font.render(line, True, ORANGE)
            else:
                text = self.small_font.render(line, True, WHITE)
            
            self.screen.blit(text, (10, y))
            y += 25 if line else 15
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.camera.dragging = True
                    self.camera.last_mouse_pos = event.pos
                elif event.button == 3:  # Right click
                    self.add_random_particles(1)
                elif event.button == 4:  # Scroll up
                    self.camera.zoom(1)
                elif event.button == 5:  # Scroll down
                    self.camera.zoom(-1)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.camera.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.camera.dragging and self.camera.last_mouse_pos:
                    dx = event.pos[0] - self.camera.last_mouse_pos[0]
                    dy = event.pos[1] - self.camera.last_mouse_pos[1]
                    self.camera.rotate(dx, dy)
                    self.camera.last_mouse_pos = event.pos
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.particles.clear()
                    self.add_random_particles(8)
    
    def update(self, dt):
        """Update simulation"""
        if self.paused:
            return
        
        # Update particles
        for particle in self.particles:
            particle.update(dt)
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.alive]
        
        # Auto-add particles if too few
        if len(self.particles) < 3:
            self.add_random_particles(1)
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    print("="*60)
    print("  3D BLACK HOLE SIMULATION - PYGAME VERSION")
    print("="*60)
    print("\nStarting fast 3D visualization...")
    print("\nControls:")
    print("  • Left-click and drag to rotate")
    print("  • Scroll to zoom")
    print("  • Right-click to add particles")
    print("  • SPACE to pause/resume")
    print("  • R to reset")
    print("  • ESC to quit")
    print("\nLaunching window...\n")
    
    sim = BlackHoleSimulation()
    sim.run()


if __name__ == "__main__":
    main()
