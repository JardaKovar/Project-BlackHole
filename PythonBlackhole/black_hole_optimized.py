"""
Optimized Black Hole Raytracer
High-performance real-time rendering with proper visuals
"""

import pygame
import numpy as np
import math
import sys
from numba import jit, prange

pygame.init()

WIDTH, HEIGHT = 800, 600  # Smaller for better FPS
FPS = 60

@jit(nopython=True, parallel=True, fastmath=True, cache=True)
def raytrace_optimized(width, height, cam_angle_x, cam_angle_y, cam_dist):
    """Ultra-optimized raytracing"""
    result = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Constants
    rs = 2.0  # Schwarzschild radius
    aspect = width / height
    
    # Precompute camera rotation
    cos_y = math.cos(cam_angle_y)
    sin_y = math.sin(cam_angle_y)
    cos_x = math.cos(cam_angle_x)
    sin_x = math.sin(cam_angle_x)
    
    for y in prange(height):
        for x in range(width):
            # Ray direction in camera space
            px = (2.0 * x / width - 1.0) * aspect
            py = 1.0 - 2.0 * y / height
            
            # Ray direction
            rd_x = px
            rd_y = py
            rd_z = 2.0
            
            # Normalize
            inv_len = 1.0 / math.sqrt(rd_x*rd_x + rd_y*rd_y + rd_z*rd_z)
            rd_x *= inv_len
            rd_y *= inv_len
            rd_z *= inv_len
            
            # Rotate ray
            rx = rd_x * cos_y - rd_z * sin_y
            rz = rd_x * sin_y + rd_z * cos_y
            ry = rd_y * cos_x - rz * sin_x
            rz = rd_y * sin_x + rz * cos_x
            
            # Ray origin
            ro_x = 0.0
            ro_y = 0.0
            ro_z = -cam_dist
            
            # Raymarching
            t = 0.0
            for _ in range(100):
                # Current position
                pos_x = ro_x + rx * t
                pos_y = ro_y + ry * t
                pos_z = ro_z + rz * t
                
                r = math.sqrt(pos_x*pos_x + pos_y*pos_y + pos_z*pos_z)
                
                # Hit event horizon
                if r < rs:
                    result[y, x, 0] = 0
                    result[y, x, 1] = 0
                    result[y, x, 2] = 0
                    break
                
                # Check accretion disk
                r_disk = math.sqrt(pos_x*pos_x + pos_z*pos_z)
                if 3.0 < r_disk < 12.0 and abs(pos_y) < 0.2:
                    # Hit disk
                    temp = 1.0 - (r_disk - 3.0) / 9.0
                    temp = temp * temp
                    
                    if temp > 0.8:
                        result[y, x] = (255, 255, 220)
                    elif temp > 0.6:
                        result[y, x] = (255, 220, 150)
                    elif temp > 0.4:
                        result[y, x] = (255, 180, 80)
                    elif temp > 0.2:
                        result[y, x] = (255, 120, 30)
                    else:
                        result[y, x] = (180, 60, 10)
                    break
                
                # Gravitational bending
                if r > rs:
                    bend = rs * rs / (r * r * r)
                    rx -= pos_x * bend * 0.5
                    ry -= pos_y * bend * 0.5
                    rz -= pos_z * bend * 0.5
                    
                    # Renormalize
                    inv_len = 1.0 / math.sqrt(rx*rx + ry*ry + rz*rz)
                    rx *= inv_len
                    ry *= inv_len
                    rz *= inv_len
                
                # Step
                t += 0.3
                
                if t > 50.0:
                    # Background
                    result[y, x, 0] = 5
                    result[y, x, 1] = 5
                    result[y, x, 2] = 15
                    break
    
    return result


class FastBlackHole:
    """Fast black hole renderer"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Black Hole - Optimized")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        
        self.angle_x = 0.4
        self.angle_y = 0.0
        self.distance = 25.0
        self.dragging = False
        self.last_pos = None
        self.running = True
        
        print("Compiling (first frame will be slow)...")
        
    def render(self):
        """Render frame"""
        pixels = raytrace_optimized(WIDTH, HEIGHT, self.angle_x, self.angle_y, self.distance)
        return pygame.surfarray.make_surface(pixels.swapaxes(0, 1))
    
    def draw(self):
        """Draw"""
        surf = self.render()
        self.screen.blit(surf, (0, 0))
        
        # FPS
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    
    def handle_events(self):
        """Input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
                    self.last_pos = event.pos
                elif event.button == 4:
                    self.distance *= 0.9
                elif event.button == 5:
                    self.distance *= 1.1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging and self.last_pos:
                    dx = event.pos[0] - self.last_pos[0]
                    dy = event.pos[1] - self.last_pos[1]
                    self.angle_y += dx * 0.01
                    self.angle_x += dy * 0.01
                    self.last_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        """Main loop"""
        frame = 0
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()
            
            frame += 1
            if frame == 1:
                print("Ready! Drag to rotate.")
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("="*50)
    print("  OPTIMIZED BLACK HOLE RAYTRACER")
    print("="*50)
    print("\nDrag mouse to rotate")
    print("Scroll to zoom")
    print("ESC to quit\n")
    
    FastBlackHole().run()
