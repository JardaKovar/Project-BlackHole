"""
Real-Time Black Hole Raytracer
Based on Schwarzschild black hole with gravitational lensing
Optimized for real-time performance
"""

import pygame
import numpy as np
import math
import sys
from numba import jit, prange
import time

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

@jit(nopython=True, parallel=True, fastmath=True)
def raytrace_frame(width, height, angle_x, angle_y, distance, time_val):
    """Raytrace entire frame in parallel"""
    pixels = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Black hole parameters
    rs = 1.0  # Schwarzschild radius (normalized)
    disk_inner = 3.0 * rs
    disk_outer = 8.0 * rs
    
    aspect = width / height
    fov = 1.2
    
    # Precompute rotation matrices
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    
    for py in prange(height):
        for px in range(width):
            # Screen to NDC
            ndc_x = (2.0 * px / width - 1.0) * aspect * fov
            ndc_y = (1.0 - 2.0 * py / height) * fov
            
            # Ray direction
            dx = ndc_x
            dy = ndc_y
            dz = 1.0
            
            # Normalize
            length = math.sqrt(dx*dx + dy*dy + dz*dz)
            dx /= length
            dy /= length
            dz /= length
            
            # Rotate ray
            dx_rot = dx * cos_y - dz * sin_y
            dz_rot = dx * sin_y + dz * cos_y
            dy_rot = dy * cos_x - dz_rot * sin_x
            dz_final = dy * sin_x + dz_rot * cos_x
            
            # Ray origin
            ox = 0.0
            oy = 0.0
            oz = -distance
            
            # Raytrace
            dt = 0.1
            max_steps = 150
            hit_disk = False
            disk_color = (0, 0, 0)
            
            for step in range(max_steps):
                r = math.sqrt(ox*ox + oy*oy + oz*oz)
                
                # Hit event horizon
                if r < rs * 1.5:
                    pixels[py, px, 0] = 0
                    pixels[py, px, 1] = 0
                    pixels[py, px, 2] = 0
                    break
                
                # Escaped
                if r > 50:
                    # Starfield background
                    star_x = int((math.atan2(dx_rot, dz_final) / math.pi + 1) * 500) % 500
                    star_y = int((math.asin(dy_rot) / math.pi + 0.5) * 500) % 500
                    if (star_x * 37 + star_y * 17) % 100 < 2:
                        pixels[py, px, 0] = 255
                        pixels[py, px, 1] = 255
                        pixels[py, px, 2] = 255
                    else:
                        pixels[py, px, 0] = 5
                        pixels[py, px, 1] = 5
                        pixels[py, px, 2] = 10
                    break
                
                # Gravitational deflection
                if r > rs:
                    accel = -2.0 * rs / (r * r * r)
                    dx_rot += accel * ox * dt
                    dy_rot += accel * oy * dt
                    dz_final += accel * oz * dt
                    
                    # Renormalize
                    length = math.sqrt(dx_rot*dx_rot + dy_rot*dy_rot + dz_final*dz_final)
                    dx_rot /= length
                    dy_rot /= length
                    dz_final /= length
                
                # Update position
                ox += dx_rot * dt
                oy += dy_rot * dt
                oz += dz_final * dt
                
                # Check disk intersection
                r_disk = math.sqrt(ox*ox + oz*oz)
                if disk_inner < r_disk < disk_outer and abs(oy) < 0.1:
                    # Hit disk
                    temp = 1.0 - (r_disk - disk_inner) / (disk_outer - disk_inner)
                    temp = temp ** 0.5
                    
                    # Doppler shift (simplified)
                    angle_disk = math.atan2(oz, ox)
                    velocity_factor = math.sin(angle_disk + time_val * 0.5) * 0.3
                    temp = temp * (1.0 + velocity_factor)
                    temp = max(0.0, min(1.0, temp))
                    
                    if temp > 0.8:
                        r, g, b = 255, 255, 240
                    elif temp > 0.6:
                        r, g, b = 255, 230, 180
                    elif temp > 0.4:
                        r, g, b = 255, 200, 100
                    elif temp > 0.2:
                        r, g, b = 255, 140, 40
                    else:
                        r, g, b = 200, 60, 10
                    
                    pixels[py, px, 0] = r
                    pixels[py, px, 1] = g
                    pixels[py, px, 2] = b
                    break
    
    return pixels


class RealtimeBlackHole:
    """Real-time black hole raytracer"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Real-Time Black Hole Raytracer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.angle_x = 0.5
        self.angle_y = 0.0
        self.distance = 20.0
        self.dragging = False
        self.last_mouse_pos = None
        self.running = True
        self.time = 0.0
        
        # Render at lower resolution for speed
        self.render_scale = 3
        self.render_width = WIDTH // self.render_scale
        self.render_height = HEIGHT // self.render_scale
        
        print("Starting real-time raytracer...")
        print("Compiling JIT functions (first frame will be slow)...")
        
    def render_frame(self):
        """Render current frame"""
        pixels = raytrace_frame(
            self.render_width,
            self.render_height,
            self.angle_x,
            self.angle_y,
            self.distance,
            self.time
        )
        
        # Convert to surface and scale up
        surf = pygame.surfarray.make_surface(pixels.swapaxes(0, 1))
        return pygame.transform.scale(surf, (WIDTH, HEIGHT))
    
    def draw(self):
        """Draw frame"""
        # Render
        frame_surf = self.render_frame()
        self.screen.blit(frame_surf, (0, 0))
        
        # Info overlay
        fps = int(self.clock.get_fps())
        fps_text = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        info_text = self.font.render("Drag: Rotate | Scroll: Zoom | ESC: Quit", True, (200, 200, 200))
        self.screen.blit(info_text, (10, HEIGHT - 30))
        
        pygame.display.flip()
    
    def handle_events(self):
        """Handle input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
                    self.last_mouse_pos = event.pos
                elif event.button == 4:
                    self.distance *= 0.9
                    self.distance = max(10, self.distance)
                elif event.button == 5:
                    self.distance *= 1.1
                    self.distance = min(40, self.distance)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging and self.last_mouse_pos:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.angle_y += dx * 0.005
                    self.angle_x += dy * 0.005
                    self.angle_x = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.angle_x))
                    self.last_mouse_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        """Main loop"""
        frame_count = 0
        start_time = time.time()
        
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.time += dt
            
            self.handle_events()
            self.draw()
            
            frame_count += 1
            if frame_count == 1:
                print(f"First frame rendered! (JIT compilation complete)")
            elif frame_count % 60 == 0:
                elapsed = time.time() - start_time
                avg_fps = frame_count / elapsed
                print(f"Average FPS: {avg_fps:.1f}")
        
        pygame.quit()
        sys.exit()


def main():
    print("="*60)
    print("  REAL-TIME BLACK HOLE RAYTRACER")
    print("="*60)
    print("\nFeatures:")
    print("  • Real-time gravitational lensing")
    print("  • Schwarzschild black hole")
    print("  • Accretion disk with Doppler shift")
    print("  • Starfield background")
    print("  • Smooth mouse rotation")
    print("  • 30-60 FPS target")
    print("\nControls:")
    print("  • Drag to rotate")
    print("  • Scroll to zoom")
    print("  • ESC to quit")
    print("\nNote: First frame will be slow (JIT compilation)")
    print("\nLaunching...\n")
    
    sim = RealtimeBlackHole()
    sim.run()


if __name__ == "__main__":
    main()
