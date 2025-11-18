"""
Black Hole Simulation - EHT Style
Optimized for 60 FPS with gravitational lensing appearance
"""

import pygame
import numpy as np
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class BlackHoleEHT:
    """Black hole with EHT-style appearance"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Black Hole - EHT Style")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.angle_y = 0
        self.angle_x = 0.3
        self.distance = 180
        self.dragging = False
        self.last_mouse_pos = None
        self.running = True
        self.paused = False
        
        # Pre-generate accretion disk (optimized)
        self.generate_disk()
        
    def generate_disk(self):
        """Generate accretion disk particles - high density for smooth appearance"""
        self.disk_particles = []
        
        # Dense disk for smooth appearance
        for radius in range(12, 50, 1):  # More rings
            segments = 40  # More segments per ring
            for i in range(segments):
                angle = (i / segments) * 2 * math.pi
                
                # Position in disk plane
                x = radius * math.cos(angle)
                z = radius * math.sin(angle)
                y = np.random.normal(0, 0.2)  # Very thin disk
                
                # Temperature (hotter closer to center)
                temp = 1.0 - (radius - 12) / 38
                
                self.disk_particles.append({
                    'x': x, 'y': y, 'z': z,
                    'angle': angle,
                    'radius': radius,
                    'temp': temp
                })
    
    def project(self, x, y, z):
        """Fast 3D projection"""
        # Rotate Y
        cos_y, sin_y = math.cos(self.angle_y), math.sin(self.angle_y)
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        # Rotate X
        cos_x, sin_x = math.cos(self.angle_x), math.sin(self.angle_x)
        y_rot = y * cos_x - z_rot * sin_x
        z_final = y * sin_x + z_rot * cos_x + self.distance
        
        if z_final <= 0:
            return None
        
        scale = 700 / z_final
        sx = int(WIDTH / 2 + x_rot * scale)
        sy = int(HEIGHT / 2 - y_rot * scale)
        
        return (sx, sy, z_final)
    
    def update_disk(self, dt):
        """Update disk rotation"""
        if self.paused:
            return
        
        rotation_speed = 0.3 * dt
        for p in self.disk_particles:
            p['angle'] += rotation_speed / p['radius']
            p['x'] = p['radius'] * math.cos(p['angle'])
            p['z'] = p['radius'] * math.sin(p['angle'])
    
    def draw(self):
        """Optimized drawing"""
        self.screen.fill(BLACK)
        
        # Project and sort particles
        projected = []
        for p in self.disk_particles:
            proj = self.project(p['x'], p['y'], p['z'])
            if proj and 0 <= proj[0] < WIDTH and 0 <= proj[1] < HEIGHT:
                projected.append((proj, p))
        
        # Sort by depth
        projected.sort(key=lambda x: -x[0][2])
        
        # Draw particles with smooth glow (multiple layers for blur effect)
        for proj, p in projected:
            temp = p['temp']
            
            # EHT-style colors
            if temp > 0.85:
                color = (255, 255, 200)  # White-yellow
            elif temp > 0.7:
                color = (255, 220, 100)  # Yellow
            elif temp > 0.5:
                color = (255, 180, 50)   # Orange-yellow
            elif temp > 0.3:
                color = (255, 120, 0)    # Orange
            else:
                color = (200, 50, 0)     # Dark orange-red
            
            # Size based on distance and temperature
            base_size = max(2, int((1000 / proj[2]) * (2 + temp * 2)))
            
            # Multi-layer glow for smooth appearance
            for layer in range(4, 0, -1):
                alpha = 0.3 / layer
                glow_size = base_size + layer * 2
                glow_color = tuple(int(c * alpha) for c in color)
                pygame.draw.circle(self.screen, glow_color, (proj[0], proj[1]), glow_size)
            
            # Bright center
            pygame.draw.circle(self.screen, color, (proj[0], proj[1]), base_size)
        
        # Draw black hole shadow
        center = self.project(0, 0, 0)
        if center:
            shadow_radius = int(700 / center[2] * 10)
            if shadow_radius > 0:
                # Black center
                pygame.draw.circle(self.screen, BLACK, (center[0], center[1]), shadow_radius)
                # Subtle edge
                pygame.draw.circle(self.screen, (30, 10, 0), (center[0], center[1]), shadow_radius, 2)
        
        # Info
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))
        
        info = self.font.render("Drag: Rotate | Scroll: Zoom | SPACE: Pause | ESC: Quit", True, (150, 150, 150))
        self.screen.blit(info, (10, HEIGHT - 30))
        
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
                    self.distance = max(100, self.distance)
                elif event.button == 5:
                    self.distance *= 1.1
                    self.distance = min(300, self.distance)
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
                elif event.key == pygame.K_r:
                    self.generate_disk()
    
    def run(self):
        """Main loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update_disk(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    print("="*60)
    print("  BLACK HOLE SIMULATION - EHT STYLE")
    print("="*60)
    print("\nOptimized for 60 FPS")
    print("Appearance similar to Event Horizon Telescope image")
    print("\nControls:")
    print("  • Drag to rotate")
    print("  • Scroll to zoom")
    print("  • SPACE to pause")
    print("  • R to reset")
    print("  • ESC to quit")
    print("\nLaunching...\n")
    
    sim = BlackHoleEHT()
    sim.run()


if __name__ == "__main__":
    main()
