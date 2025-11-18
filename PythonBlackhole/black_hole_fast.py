"""
Fast Black Hole Visualization
Uses pre-computed lookup table for real-time 60 FPS rendering
"""

import pygame
import numpy as np
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

class FastBlackHole:
    """Fast black hole using pre-computed textures"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Black Hole - Fast Rendering")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.angle_x = 0.3
        self.angle_y = 0.0
        self.distance = 15.0
        self.dragging = False
        self.last_pos = None
        self.running = True
        
        # Pre-generate black hole texture
        print("Generating black hole texture...")
        self.texture = self.generate_texture()
        self.surf = pygame.surfarray.make_surface(self.texture)
        print("Ready!")
        
    def generate_texture(self):
        """Generate black hole appearance as texture"""
        tex = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        
        cx, cy = WIDTH // 2, HEIGHT // 2
        
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - cx
                dy = y - cy
                r = math.sqrt(dx*dx + dy*dy)
                
                # Normalize
                r_norm = r / (min(WIDTH, HEIGHT) * 0.35)
                
                # Add some asymmetry for 3D effect
                angle = math.atan2(dy, dx)
                asymmetry = 1.0 + 0.15 * math.sin(angle * 2)
                r_norm *= asymmetry
                
                if r_norm < 0.18:
                    # Event horizon - pure black
                    tex[y, x] = (0, 0, 0)
                elif r_norm < 0.22:
                    # Photon sphere edge - sharp bright ring
                    t = (r_norm - 0.18) / 0.04
                    intensity = int(255 * (1 - t))
                    tex[y, x] = (intensity, intensity, intensity)
                elif r_norm < 0.35:
                    # Inner accretion disk - white hot
                    t = (r_norm - 0.22) / 0.13
                    t = t ** 0.7  # Non-linear falloff
                    r_val = 255
                    g_val = int(255 * (1 - t * 0.15))
                    b_val = int(255 * (1 - t * 0.4))
                    tex[y, x] = (r_val, g_val, b_val)
                elif r_norm < 0.55:
                    # Mid disk - yellow to orange
                    t = (r_norm - 0.35) / 0.2
                    t = t ** 0.8
                    r_val = 255
                    g_val = int(255 * (1 - t * 0.4))
                    b_val = int(200 * (1 - t * 0.8))
                    tex[y, x] = (r_val, g_val, b_val)
                elif r_norm < 0.85:
                    # Outer disk - orange to red
                    t = (r_norm - 0.55) / 0.3
                    t = t ** 0.9
                    r_val = int(255 * (1 - t * 0.2))
                    g_val = int(180 * (1 - t * 0.7))
                    b_val = int(80 * (1 - t * 0.9))
                    tex[y, x] = (r_val, g_val, b_val)
                elif r_norm < 1.1:
                    # Far outer disk - deep red fading
                    t = (r_norm - 0.85) / 0.25
                    t = t ** 1.2
                    r_val = int(200 * (1 - t))
                    g_val = int(60 * (1 - t))
                    b_val = int(20 * (1 - t))
                    tex[y, x] = (r_val, g_val, b_val)
                else:
                    # Background - dark space
                    tex[y, x] = (2, 2, 8)
        
        # Add glow and lensing effects
        self.add_glow(tex, cx, cy)
        self.add_lensing_ring(tex, cx, cy)
        
        return tex.swapaxes(0, 1)
    
    def add_glow(self, tex, cx, cy):
        """Add glow effect"""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - cx
                dy = y - cy
                r = math.sqrt(dx*dx + dy*dy)
                r_norm = r / (min(WIDTH, HEIGHT) * 0.35)
                
                if 0.18 < r_norm < 1.3:
                    glow = max(0, 1.0 - (r_norm - 0.18) / 1.12)
                    glow = glow ** 2.5
                    
                    tex[y, x, 0] = min(255, int(tex[y, x, 0] + glow * 60))
                    tex[y, x, 1] = min(255, int(tex[y, x, 1] + glow * 40))
                    tex[y, x, 2] = min(255, int(tex[y, x, 2] + glow * 15))
    
    def add_lensing_ring(self, tex, cx, cy):
        """Add gravitational lensing ring effect"""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - cx
                dy = y - cy
                r = math.sqrt(dx*dx + dy*dy)
                r_norm = r / (min(WIDTH, HEIGHT) * 0.35)
                
                # Einstein ring effect
                if 0.17 < r_norm < 0.19:
                    ring_intensity = 1.0 - abs(r_norm - 0.18) / 0.01
                    ring_intensity = ring_intensity ** 3
                    
                    tex[y, x, 0] = min(255, int(tex[y, x, 0] + ring_intensity * 100))
                    tex[y, x, 1] = min(255, int(tex[y, x, 1] + ring_intensity * 80))
                    tex[y, x, 2] = min(255, int(tex[y, x, 2] + ring_intensity * 60))
    
    def draw(self):
        """Draw frame"""
        # Rotate texture
        rotated = pygame.transform.rotate(self.surf, self.angle_y * 57.3)
        
        # Center it
        rect = rotated.get_rect(center=(WIDTH//2, HEIGHT//2))
        
        # Draw
        self.screen.fill((0, 0, 5))
        self.screen.blit(rotated, rect)
        
        # FPS
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        info_text = self.font.render("Drag to rotate | Scroll to zoom | ESC to quit", True, (200, 200, 200))
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
                    self.angle_y += dx * 0.01
                    self.last_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        """Main loop"""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("="*60)
    print("  FAST BLACK HOLE VISUALIZATION")
    print("="*60)
    print("\nFeatures:")
    print("  • 60 FPS smooth rendering")
    print("  • Pre-computed textures")
    print("  • Smooth rotation")
    print("  • Improved visuals with:")
    print("    - Sharp photon sphere ring")
    print("    - Better color gradients")
    print("    - Enhanced glow effect")
    print("    - Einstein ring lensing")
    print("    - 3D asymmetry")
    print("\nControls:")
    print("  • Drag to rotate")
    print("  • Scroll to zoom")
    print("  • ESC to quit\n")
    
    FastBlackHole().run()
