"""
Advanced Gravitational Lensing Renderer
Creates a realistic black hole visualization with light bending effects
"""

import math
import numpy as np
from config import *
from utils import *


class LensingRenderer:
    """Renders black hole with gravitational lensing effects"""
    
    def __init__(self, width=120, height=40):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Color palette for accretion disk (temperature gradient)
        self.colors = {
            'black': '\033[38;5;0m',
            'dark_red': '\033[38;5;52m',
            'red': '\033[38;5;88m',
            'orange_red': '\033[38;5;124m',
            'orange': '\033[38;5;166m',
            'yellow_orange': '\033[38;5;208m',
            'yellow': '\033[38;5;220m',
            'bright_yellow': '\033[38;5;226m',
            'white': '\033[38;5;231m',
            'reset': '\033[0m'
        }
        
        # Brightness characters (from dark to bright)
        self.brightness_chars = ' .:-=+*#%@'
        
        # Pre-calculate the lensing effect
        self.intensity_map = np.zeros((height, width))
        self.color_map = [[self.colors['black'] for _ in range(width)] for _ in range(height)]
        self.char_map = [[' ' for _ in range(width)] for _ in range(height)]
        
    def calculate_lensing(self, black_hole):
        """Calculate gravitational lensing effect"""
        rs = black_hole.schwarzschild_radius
        
        # Scale factor for visualization
        scale = 15.0  # Show region up to 15 Rs
        
        for y in range(self.height):
            for x in range(self.width):
                # Convert screen coordinates to physical coordinates
                px = (x - self.center_x) / (self.width / (2 * scale))
                py = (y - self.center_y) / (self.height / (2 * scale)) * 2  # Aspect ratio correction
                
                # Distance from center in Schwarzschild radii
                r = math.sqrt(px**2 + py**2)
                
                if r < 0.01:
                    r = 0.01
                
                # Calculate intensity based on distance and lensing
                intensity = 0.0
                color = self.colors['black']
                char = ' '
                
                # Event horizon (pure black)
                if r <= 1.0:
                    intensity = 0.0
                    color = self.colors['black']
                    char = '█'
                
                # Photon sphere region (bright ring)
                elif r <= 1.8:
                    # Photon ring - very bright
                    ring_intensity = 1.0 - abs(r - 1.5) / 0.3
                    ring_intensity = max(0, ring_intensity) ** 2
                    intensity = ring_intensity * 0.9
                    
                    if intensity > 0.8:
                        color = self.colors['bright_yellow']
                    elif intensity > 0.6:
                        color = self.colors['yellow']
                    elif intensity > 0.4:
                        color = self.colors['yellow_orange']
                    else:
                        color = self.colors['orange']
                
                # Accretion disk region
                elif r <= 8.0:
                    # Check if in disk plane (thin disk)
                    disk_thickness = 0.3 + r * 0.05
                    if abs(py) < disk_thickness:
                        # Temperature decreases with radius
                        temp_factor = (8.0 - r) / 7.0
                        
                        # Doppler boosting (one side brighter)
                        doppler_boost = 1.0 + 0.3 * px / r if r > 0 else 1.0
                        
                        # Gravitational lensing amplification
                        lensing_factor = 1.0 / (1.0 + (r - 2.0) * 0.1)
                        
                        intensity = temp_factor * doppler_boost * lensing_factor * 0.7
                        intensity = min(1.0, max(0.0, intensity))
                        
                        # Color based on temperature
                        if intensity > 0.7:
                            color = self.colors['yellow']
                        elif intensity > 0.5:
                            color = self.colors['yellow_orange']
                        elif intensity > 0.3:
                            color = self.colors['orange']
                        elif intensity > 0.15:
                            color = self.colors['orange_red']
                        else:
                            color = self.colors['red']
                    else:
                        # Above/below disk - scattered light
                        scatter_intensity = 0.1 / (abs(py) + 0.5)
                        scatter_intensity *= (8.0 - r) / 7.0
                        intensity = scatter_intensity * 0.3
                        
                        if intensity > 0.1:
                            color = self.colors['dark_red']
                        else:
                            color = self.colors['black']
                
                # Outer glow
                elif r <= 12.0:
                    glow_intensity = (12.0 - r) / 4.0
                    glow_intensity = glow_intensity ** 2 * 0.2
                    intensity = glow_intensity
                    
                    if intensity > 0.05:
                        color = self.colors['dark_red']
                    else:
                        color = self.colors['black']
                
                # Store calculated values
                self.intensity_map[y][x] = intensity
                self.color_map[y][x] = color
                
                # Choose character based on intensity
                char_index = int(intensity * (len(self.brightness_chars) - 1))
                char_index = max(0, min(len(self.brightness_chars) - 1, char_index))
                self.char_map[y][x] = self.brightness_chars[char_index]
    
    def render(self, black_hole):
        """Render the black hole with lensing effects"""
        # Calculate lensing (only once or when needed)
        self.calculate_lensing(black_hole)
        
        # Build output
        output = []
        for y in range(self.height):
            line = ""
            current_color = self.colors['reset']
            
            for x in range(self.width):
                color = self.color_map[y][x]
                char = self.char_map[y][x]
                
                if color != current_color:
                    line += color
                    current_color = color
                
                line += char
            
            line += self.colors['reset']
            output.append(line)
        
        return '\n'.join(output)
    
    def render_with_info(self, black_hole, simulation_time, fps, particle_count):
        """Render with information overlay"""
        image = self.render(black_hole)
        
        # Add info text
        info_lines = [
            "",
            f"  BLACK HOLE VISUALIZATION",
            f"  Mass: {format_mass(black_hole.mass)}",
            f"  Schwarzschild Radius: {format_distance(black_hole.schwarzschild_radius)}",
            f"  Temperature: {format_temperature(black_hole.temperature)}",
            f"",
            f"  Simulation Time: {simulation_time:.1f}s",
            f"  FPS: {fps:.1f}",
            f"  Particles: {particle_count}",
            f"",
            f"  Press Q to quit, SPACE to add particle",
            ""
        ]
        
        return image + '\n' + '\n'.join(info_lines)
