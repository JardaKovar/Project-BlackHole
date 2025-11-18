"""
Black Hole Raytracer
Real gravitational lensing simulation using raytracing
"""

import pygame
import numpy as np
import math
import sys
from numba import jit

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

@jit(nopython=True)
def raytrace_pixel(px, py, width, height, angle_x, angle_y, distance):
    """Raytrace a single pixel through curved spacetime"""
    # Screen to camera ray
    aspect = width / height
    fov = 0.8
    
    # Normalized device coordinates
    ndc_x = (2.0 * px / width - 1.0) * aspect * fov
    ndc_y = (1.0 - 2.0 * py / height) * fov
    
    # Camera rotation
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    
    # Ray direction
    dx = ndc_x
    dy = ndc_y
    dz = 1.0
    
    # Rotate ray
    dx_rot = dx * cos_y - dz * sin_y
    dz_rot = dx * sin_y + dz * cos_y
    dy_rot = dy * cos_x - dz_rot * sin_x
    dz_final = dy * sin_x + dz_rot * cos_x
    
    # Normalize
    length = math.sqrt(dx_rot**2 + dy_rot**2 + dz_final**2)
    dx_rot /= length
    dy_rot /= length
    dz_final /= length
    
    # Ray origin (camera position)
    ox = 0.0
    oy = 0.0
    oz = -distance
    
    # Schwarzschild radius
    rs = 10.0
    
    # Raytrace through curved spacetime
    dt = 0.5
    max_steps = 200
    
    for step in range(max_steps):
        # Current position
        r = math.sqrt(ox**2 + oy**2 + oz**2)
        
        # Check if hit event horizon
        if r < rs * 1.1:
            return (0, 0, 0)  # Black
        
        # Check if escaped
        if r > 200:
            return (0, 0, 0)  # Background
        
        # Gravitational deflection (simplified Schwarzschild metric)
        if r > rs:
            # Acceleration towards black hole
            accel = -1.5 * rs**2 / r**3
            
            # Update velocity (gravitational bending)
            dx_rot += accel * ox * dt
            dy_rot += accel * oy * dt
            dz_final += accel * oz * dt
            
            # Renormalize (keep speed constant)
            length = math.sqrt(dx_rot**2 + dy_rot**2 + dz_final**2)
            dx_rot /= length
            dy_rot /= length
            dz_final /= length
        
        # Update position
        ox += dx_rot * dt
        oy += dy_rot * dt
        oz += dz_final * dt
        
        # Check if ray hits accretion disk
        disk_inner = rs * 1.5
        disk_outer = rs * 4.0
        disk_thickness = 0.5
        
        r_disk = math.sqrt(ox**2 + oz**2)
        
        if disk_inner < r_disk < disk_outer and abs(oy) < disk_thickness:
            # Hit disk - calculate color based on radius
            temp = 1.0 - (r_disk - disk_inner) / (disk_outer - disk_inner)
            temp = temp ** 0.6
            
            if temp > 0.9:
                return (255, 255, 240)
            elif temp > 0.75:
                return (255, 240, 180)
            elif temp > 0.6:
                return (255, 220, 120)
            elif temp > 0.4:
                return (255, 180, 60)
            elif temp > 0.2:
                return (255, 120, 20)
            else:
                return (200, 60, 0)
    
    return (0, 0, 0)


class BlackHoleRaytracer:
    """Real raytracing black hole"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Black Hole Raytracer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.angle_x = 0.3
        self.angle_y = 0.0
        self.distance = 80
        self.dragging = False
        self.last_mouse_pos = None
        self.running = True
        
        # Render buffer
        self.render_scale = 2  # Render at half resolution for speed
        self.render_width = WIDTH // self.render_scale
        self.render_height = HEIGHT // self.render_scale
        
        print("Rendering initial frame...")
        self.render_frame()
        
    def render_frame(self):
        """Render the black hole using raytracing"""
        # Create pixel array
        pixels = np.zeros((self.render_height, self.render_width, 3), dtype=np.uint8)
        
        # Raytrace each pixel
        for y in range(self.render_height):
            for x in range(self.render_width):
                color = raytrace_pixel(
                    x, y,
                    self.render_width, self.render_height,
                    self.angle_x, self.angle_y, self.distance
                )
                pixels[y, x] = color
            
            # Show progress
            if y % 20 == 0:
                print(f"Rendering: {int(100 * y / self.render_height)}%")
        
        # Convert to surface and scale up
        surf = pygame.surfarray.make_surface(pixels.swapaxes(0, 1))
        self.rendered_surface = pygame.transform.scale(surf, (WIDTH, HEIGHT))
        
        print("Render complete!")
    
    def draw(self):
        """Display rendered frame"""
        self.screen.fill((0, 0, 0))
        
        if hasattr(self, 'rendered_surface'):
            self.screen.blit(self.rendered_surface, (0, 0))
        
        # Info
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        info_text = self.font.render("Drag to rotate (will re-render) | Scroll: Zoom | ESC: Quit", True, (150, 150, 150))
        self.screen.blit(info_text, (10, HEIGHT - 30))
        
        pygame.display.flip()
    
    def handle_events(self):
        """Handle input"""
        need_rerender = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
                    self.last_mouse_pos = event.pos
                elif event.button == 4:
                    self.distance *= 0.9
                    self.distance = max(50, self.distance)
                    need_rerender = True
                elif event.button == 5:
                    self.distance *= 1.1
                    self.distance = min(150, self.distance)
                    need_rerender = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                    if self.last_mouse_pos:
                        need_rerender = True
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
        
        if need_rerender:
            print("\nRe-rendering...")
            self.render_frame()
    
    def run(self):
        """Main loop"""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    print("="*60)
    print("  BLACK HOLE RAYTRACER")
    print("="*60)
    print("\nReal gravitational lensing simulation")
    print("Uses raytracing through curved spacetime")
    print("\nFeatures:")
    print("  • Proper light bending")
    print("  • Accretion disk visible front AND back")
    print("  • Schwarzschild metric")
    print("  • Event horizon shadow")
    print("\nControls:")
    print("  • Drag to rotate (triggers re-render)")
    print("  • Scroll to zoom")
    print("  • ESC to quit")
    print("\nNote: Rendering takes a few seconds...")
    print("\nLaunching...\n")
    
    try:
        sim = BlackHoleRaytracer()
        sim.run()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
