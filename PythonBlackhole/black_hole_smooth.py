"""
Black Hole Simulation - True EHT Style with Smooth Rendering
Uses surface blending for authentic smooth appearance
"""

import pygame
import numpy as np
import math
import sys
from pygame import gfxdraw

pygame.init()

WIDTH, HEIGHT = 1400, 900
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class BlackHoleSmooth:
    """Black hole with true smooth rendering"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Black Hole - Smooth EHT Style")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        
        # Create surface for blending
        self.glow_surface = pygame.Surface((WIDTH, HEIGHT))
        self.glow_surface.set_colorkey(BLACK)
        
        self.angle_y = 0
        self.angle_x = 0.4
        self.distance = 150
        self.dragging = False
        self.last_mouse_pos = None
        self.running = True
        self.paused = False
        self.time = 0
        
    def project(self, x, y, z):
        """Fast 3D projection"""
        cos_y, sin_y = math.cos(self.angle_y), math.sin(self.angle_y)
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        cos_x, sin_x = math.cos(self.angle_x), math.sin(self.angle_x)
        y_rot = y * cos_x - z_rot * sin_x
        z_final = y * sin_x + z_rot * cos_x + self.distance
        
        if z_final <= 0:
            return None
        
        scale = 1000 / z_final
        sx = int(WIDTH / 2 + x_rot * scale)
        sy = int(HEIGHT / 2 - y_rot * scale)
        
        return (sx, sy, z_final)
    
    def draw_smooth_disk(self):
        """Draw accretion disk with true smooth rendering"""
        self.glow_surface.fill(BLACK)
        
        # Generate disk points with high density
        for radius in np.linspace(15, 45, 60):  # 60 rings
            segments = 80  # 80 points per ring
            
            for i in range(segments):
                angle = (i / segments) * 2 * math.pi + self.time * 0.2 / radius
                
                # Position
                x = radius * math.cos(angle)
                z = radius * math.sin(angle)
                y = np.random.normal(0, 0.15)
                
                proj = self.project(x, y, z)
                if not proj or proj[0] < 0 or proj[0] >= WIDTH or proj[1] < 0 or proj[1] >= HEIGHT:
                    continue
                
                # Temperature based on radius
                temp = 1.0 - (radius - 15) / 30
                temp = max(0, min(1, temp ** 0.7))  # Power curve for better gradient
                
                # EHT colors
                if temp > 0.9:
                    color = (255, 255, 240)
                elif temp > 0.75:
                    color = (255, 240, 180)
                elif temp > 0.6:
                    color = (255, 200, 100)
                elif temp > 0.4:
                    color = (255, 150, 40)
                elif temp > 0.2:
                    color = (220, 80, 10)
                else:
                    color = (150, 40, 0)
                
                # Size and intensity based on distance
                size = int((1200 / proj[2]) * (3 + temp * 4))
                size = max(3, min(15, size))
                
                # Draw with multiple layers for smooth blend
                for layer in range(size, 0, -1):
                    alpha = int(255 * (layer / size) * 0.4)
                    layer_color = tuple(int(c * alpha / 255) for c in color)
                    
                    try:
                        gfxdraw.filled_circle(
                            self.glow_surface,
                            proj[0], proj[1],
                            layer,
                            layer_color + (alpha,)
                        )
                    except:
                        pass
        
        # Blend glow surface onto main screen
        self.screen.blit(self.glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)
    
    def draw_black_hole(self):
        """Draw black hole shadow"""
        center = self.project(0, 0, 0)
        if center:
            radius = int(1000 / center[2] * 12)
            if radius > 5:
                # Draw shadow with soft edge
                for i in range(radius + 10, radius, -1):
                    alpha = int(255 * (1 - (i - radius) / 10))
                    color = (alpha // 10, 0, 0)
                    gfxdraw.filled_circle(self.screen, center[0], center[1], i, color)
                
                # Pure black center
                gfxdraw.filled_circle(self.screen, center[0], center[1], radius, BLACK)
    
    def draw(self):
        """Main draw"""
        self.screen.fill(BLACK)
        
        # Draw disk
        self.draw_smooth_disk()
        
        # Draw black hole on top
        self.draw_black_hole()
        
        # Info
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))
        
        info = self.font.render("Drag: Rotate | Scroll: Zoom | SPACE: Pause | ESC: Quit", True, (120, 120, 120))
        self.screen.blit(info, (10, HEIGHT - 25))
        
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
                    self.distance = max(80, self.distance)
                elif event.button == 5:
                    self.distance *= 1.1
                    self.distance = min(250, self.distance)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging and self.last_mouse_pos:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.angle_y += dx * 0.003
                    self.angle_x += dy * 0.003
                    self.angle_x = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.angle_x))
                    self.last_mouse_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
    
    def run(self):
        """Main loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            if not self.paused:
                self.time += dt
            
            self.handle_events()
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    print("="*60)
    print("  BLACK HOLE - SMOOTH EHT STYLE")
    print("="*60)
    print("\nTrue smooth rendering with surface blending")
    print("Matches Event Horizon Telescope appearance")
    print("\nControls:")
    print("  • Drag to rotate")
    print("  • Scroll to zoom")
    print("  • SPACE to pause")
    print("  • ESC to quit")
    print("\nLaunching...\n")
    
    sim = BlackHoleSmooth()
    sim.run()


if __name__ == "__main__":
    main()
