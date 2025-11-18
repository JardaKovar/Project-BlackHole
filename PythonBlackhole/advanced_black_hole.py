"""
Advanced Black Hole Visualization with Full Ray Tracing
Creates a complete, rotating black hole with gravitational lensing
"""

import sys
import time
import os
import math
import numpy as np

# Initialize colorama for Windows
try:
    import colorama
    colorama.init(autoreset=False, strip=False)
except ImportError:
    pass

try:
    import msvcrt
    WINDOWS = True
except ImportError:
    WINDOWS = False


class AdvancedBlackHoleRenderer:
    """Full ray-traced black hole with rotation"""
    
    def __init__(self, width=160, height=50):
        self.width = width
        self.height = height
        self.rotation_angle = 0.0
        self.rotation_speed = 0.05
        
        # RGB-like color palette using ANSI 256 colors
        self.create_color_palette()
        
    def create_color_palette(self):
        """Create smooth color gradient for temperature"""
        self.colors = []
        # Black to dark red
        for i in range(16, 53):
            self.colors.append(f'\033[38;5;{i}m')
        # Red to orange
        for i in range(88, 231, 6):
            self.colors.append(f'\033[38;5;{i}m')
        # Orange to yellow
        for i in range(220, 231):
            self.colors.append(f'\033[38;5;{i}m')
        
        self.reset = '\033[0m'
    
    def get_color_from_intensity(self, intensity):
        """Get color based on intensity (0-1)"""
        if intensity <= 0:
            return '\033[38;5;0m'  # Black
        
        idx = int(intensity * (len(self.colors) - 1))
        idx = max(0, min(len(self.colors) - 1, idx))
        return self.colors[idx]
    
    def ray_trace_pixel(self, x, y):
        """
        Ray trace a single pixel through curved spacetime
        Returns (intensity, is_disk, distance)
        """
        # Convert screen coordinates to camera coordinates
        aspect_ratio = self.width / (self.height * 2)
        px = (x - self.width / 2) / (self.width / 2) * aspect_ratio
        py = (y - self.height / 2) / (self.height / 2)
        
        # Camera distance and field of view
        camera_dist = 20.0
        
        # Ray direction
        ray_x = px
        ray_y = py
        ray_z = -1.0
        
        # Normalize
        ray_len = math.sqrt(ray_x**2 + ray_y**2 + ray_z**2)
        ray_x /= ray_len
        ray_y /= ray_len
        ray_z /= ray_len
        
        # Ray origin (camera position)
        pos_x = 0.0
        pos_y = 0.0
        pos_z = camera_dist
        
        # Schwarzschild radius (in simulation units)
        rs = 1.0
        
        # Ray marching parameters
        max_steps = 200
        step_size = 0.1
        
        for step in range(max_steps):
            # Current distance from black hole center
            r = math.sqrt(pos_x**2 + pos_y**2 + pos_z**2)
            
            if r < 0.01:
                r = 0.01
            
            # Check if hit event horizon
            if r < rs * 1.0:
                return (0.0, False, r)  # Absorbed by black hole
            
            # Check if in accretion disk
            disk_inner = rs * 3.0  # ISCO
            disk_outer = rs * 12.0
            disk_thickness = 0.15 + r * 0.02
            
            if disk_inner < r < disk_outer and abs(pos_y) < disk_thickness:
                # In the disk
                # Calculate temperature based on radius
                temp_factor = (disk_outer - r) / (disk_outer - disk_inner)
                
                # Apply rotation (Doppler boosting)
                angle = math.atan2(pos_z, pos_x) + self.rotation_angle
                doppler = 1.0 + 0.4 * math.cos(angle)
                
                # Gravitational lensing amplification
                lensing = 1.0 / (1.0 + (r - disk_inner) * 0.05)
                
                # Final intensity
                intensity = temp_factor * doppler * lensing * 0.9
                intensity = max(0.0, min(1.0, intensity))
                
                return (intensity, True, r)
            
            # Gravitational deflection (simplified)
            if r > rs:
                # Acceleration towards black hole
                accel_factor = (rs * rs) / (r * r * r)
                
                # Deflect ray
                ray_x -= pos_x * accel_factor * step_size
                ray_y -= pos_y * accel_factor * step_size
                ray_z -= pos_z * accel_factor * step_size
                
                # Renormalize (approximately)
                ray_len = math.sqrt(ray_x**2 + ray_y**2 + ray_z**2)
                if ray_len > 0:
                    ray_x /= ray_len
                    ray_y /= ray_len
                    ray_z /= ray_len
            
            # March ray forward
            pos_x += ray_x * step_size
            pos_y += ray_y * step_size
            pos_z += ray_z * step_size
            
            # Check if ray escaped
            if r > 30.0:
                # Check for photon ring (secondary image)
                if 1.4 < r < 1.7:
                    ring_intensity = 1.0 - abs(r - 1.5) / 0.2
                    return (ring_intensity * 0.8, False, r)
                return (0.0, False, r)
        
        return (0.0, False, 0.0)
    
    def render_frame(self):
        """Render a complete frame"""
        output = []
        
        for y in range(self.height):
            line = ""
            current_color = self.reset
            
            for x in range(self.width):
                intensity, is_disk, distance = self.ray_trace_pixel(x, y)
                
                # Choose character based on intensity
                if intensity > 0.9:
                    char = '@'
                elif intensity > 0.7:
                    char = '#'
                elif intensity > 0.5:
                    char = '%'
                elif intensity > 0.3:
                    char = '+'
                elif intensity > 0.15:
                    char = '='
                elif intensity > 0.08:
                    char = '-'
                elif intensity > 0.04:
                    char = ':'
                elif intensity > 0.02:
                    char = '.'
                else:
                    char = ' '
                
                # Get color
                color = self.get_color_from_intensity(intensity)
                
                if color != current_color:
                    line += color
                    current_color = color
                
                line += char
            
            line += self.reset
            output.append(line)
        
        return '\n'.join(output)
    
    def update_rotation(self):
        """Update rotation angle"""
        self.rotation_angle += self.rotation_speed
        if self.rotation_angle > 2 * math.pi:
            self.rotation_angle -= 2 * math.pi


class BlackHoleSimulation:
    """Main simulation with rotating black hole"""
    
    def __init__(self):
        self.renderer = AdvancedBlackHoleRenderer(width=160, height=50)
        self.running = False
        self.fps = 0.0
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.fps_frames = 0
    
    def clear_screen(self):
        """Clear terminal"""
        if os.name == 'nt':
            os.system('cls')
        else:
            print('\033[2J\033[H', end='')
    
    def get_key_non_blocking(self):
        """Get key without blocking"""
        if WINDOWS:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    return key.decode('utf-8').lower()
                except:
                    return None
        return None
    
    def render(self):
        """Render frame"""
        self.clear_screen()
        
        # Render black hole
        frame = self.renderer.render_frame()
        print(frame)
        
        # Info
        print(f"\n  Rotating Black Hole with Gravitational Lensing")
        print(f"  FPS: {self.fps:.1f} | Frame: {self.frame_count}")
        print(f"  Press Q to quit, +/- to adjust rotation speed")
        
        # Update FPS
        self.fps_frames += 1
        current_time = time.time()
        if current_time - self.last_fps_time >= 1.0:
            self.fps = self.fps_frames / (current_time - self.last_fps_time)
            self.fps_frames = 0
            self.last_fps_time = current_time
    
    def run(self):
        """Main loop"""
        self.running = True
        target_frame_time = 1.0 / 30
        
        print("\n" + "="*60)
        print("  ADVANCED BLACK HOLE VISUALIZATION")
        print("="*60)
        print("\n  Rendering rotating black hole with:")
        print("  • Full ray tracing through curved spacetime")
        print("  • Gravitational lensing effects")
        print("  • Rotating accretion disk")
        print("  • Doppler boosting")
        print("  • Photon ring")
        print("\n  Press any key to start...")
        
        if WINDOWS:
            msvcrt.getch()
        else:
            input()
        
        try:
            while self.running:
                start_time = time.time()
                
                # Handle input
                key = self.get_key_non_blocking()
                if key == 'q':
                    self.running = False
                elif key == '+' or key == '=':
                    self.renderer.rotation_speed = min(0.2, self.renderer.rotation_speed + 0.01)
                elif key == '-' or key == '_':
                    self.renderer.rotation_speed = max(0.0, self.renderer.rotation_speed - 0.01)
                
                # Update
                self.renderer.update_rotation()
                
                # Render
                self.render()
                self.frame_count += 1
                
                # Frame limiting
                elapsed = time.time() - start_time
                if elapsed < target_frame_time:
                    time.sleep(target_frame_time - elapsed)
        
        except KeyboardInterrupt:
            pass
        finally:
            print("\n\n  Thank you for exploring the black hole!\n")


def main():
    """Entry point"""
    try:
        sim = BlackHoleSimulation()
        sim.run()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
