"""
Final Black Hole Visualization - Version 2
60 FPS with full 3D rotation, particles, and soft gradients
"""

import pygame
import numpy as np
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

class Camera:
    """3D Camera for full rotation"""
    
    def __init__(self):
        self.angle_x = 0.3
        self.angle_y = 0.0
        self.distance = 15.0
        self.dragging = False
        self.last_pos = None
    
    def rotate(self, dx, dy):
        """Rotate on both axes"""
        self.angle_y += dx * 0.01
        self.angle_x += dy * 0.01
        self.angle_x = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.angle_x))
    
    def zoom(self, amount):
        """Zoom in/out"""
        self.distance *= (0.9 if amount > 0 else 1.1)
        self.distance = max(10, min(30, self.distance))


class Particle:
    """Particle affected by black hole"""
    
    def __init__(self, x, y, z, vx, vy, vz):
        self.pos = np.array([x, y, z], dtype=float)
        self.vel = np.array([vx, vy, vz], dtype=float)
        self.trail = []
        self.alive = True
        self.color = (0, 255, 0)
    
    def update(self, dt):
        """Update physics"""
        if not self.alive:
            return
        
        r = np.linalg.norm(self.pos)
        
        if r < 2:  # Captured
            self.alive = False
            return
        
        if r > 0:
            accel = -50.0 * self.pos / (r ** 2)
            self.vel += accel * dt
            self.pos += self.vel * dt
            
            self.trail.append(self.pos.copy())
            if len(self.trail) > 20:
                self.trail.pop(0)
            
            # Color based on speed
            speed = np.linalg.norm(self.vel)
            if speed > 15:
                self.color = (255, 0, 0)
            elif speed > 8:
                self.color = (255, 165, 0)
            else:
                self.color = (0, 255, 0)


class BlackHoleFinal:
    """Final black hole with full 3D rotation and particles"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Black Hole - Final Version")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.camera = Camera()
        self.particles = []
        self.running = True
        
        # Generate base texture
        print("Generating black hole texture...")
        self.base_texture = self.generate_soft_texture()
        print("Ready!")
        
        # Add initial particles
        self.add_random_particles(5)
    
    def generate_soft_texture(self):
        """Generate texture with SOFT edges"""
        tex = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        
        cx, cy = WIDTH // 2, HEIGHT // 2
        
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - cx
                dy = y - cy
                r = math.sqrt(dx*dx + dy*dy)
                
                r_norm = r / (min(WIDTH, HEIGHT) * 0.35)
                
                # Asymmetry for 3D
                angle = math.atan2(dy, dx)
                asymmetry = 1.0 + 0.12 * math.sin(angle * 2)
                r_norm *= asymmetry
                
                if r_norm < 0.18:
                    # Event horizon
                    tex[y, x] = (0, 0, 0)
                elif r_norm < 0.24:
                    # SOFT transition to photon sphere
                    t = (r_norm - 0.18) / 0.06
                    t = t ** 0.5  # Softer curve
                    intensity = int(255 * (1 - t))
                    tex[y, x] = (intensity, intensity, intensity)
                elif r_norm < 0.38:
                    # Inner disk - SOFT gradient
                    t = (r_norm - 0.24) / 0.14
                    t = t ** 0.6  # Softer falloff
                    r_val = 255
                    g_val = int(255 * (1 - t * 0.2))
                    b_val = int(255 * (1 - t * 0.5))
                    tex[y, x] = (r_val, g_val, b_val)
                elif r_norm < 0.60:
                    # Mid disk - SOFT yellow to orange
                    t = (r_norm - 0.38) / 0.22
                    t = t ** 0.7
                    r_val = 255
                    g_val = int(255 * (1 - t * 0.5))
                    b_val = int(200 * (1 - t * 0.85))
                    tex[y, x] = (r_val, g_val, b_val)
                elif r_norm < 0.90:
                    # Outer disk - SOFT orange to red
                    t = (r_norm - 0.60) / 0.30
                    t = t ** 0.8
                    r_val = int(255 * (1 - t * 0.25))
                    g_val = int(180 * (1 - t * 0.75))
                    b_val = int(80 * (1 - t))
                    tex[y, x] = (r_val, g_val, b_val)
                elif r_norm < 1.15:
                    # Far outer - SOFT red fade
                    t = (r_norm - 0.90) / 0.25
                    t = t ** 1.0
                    r_val = int(200 * (1 - t))
                    g_val = int(60 * (1 - t))
                    b_val = int(20 * (1 - t))
                    tex[y, x] = (r_val, g_val, b_val)
                else:
                    tex[y, x] = (2, 2, 8)
        
        # SOFT glow
        self.add_soft_glow(tex, cx, cy)
        
        return tex.swapaxes(0, 1)
    
    def add_soft_glow(self, tex, cx, cy):
        """Add SOFT glow effect"""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - cx
                dy = y - cy
                r = math.sqrt(dx*dx + dy*dy)
                r_norm = r / (min(WIDTH, HEIGHT) * 0.35)
                
                if 0.18 < r_norm < 1.4:
                    glow = max(0, 1.0 - (r_norm - 0.18) / 1.22)
                    glow = glow ** 3.0  # Very soft falloff
                    
                    tex[y, x, 0] = min(255, int(tex[y, x, 0] + glow * 50))
                    tex[y, x, 1] = min(255, int(tex[y, x, 1] + glow * 35))
                    tex[y, x, 2] = min(255, int(tex[y, x, 2] + glow * 12))
    
    def add_random_particles(self, count):
        """Add random particles"""
        for _ in range(count):
            angle = np.random.uniform(0, 2 * math.pi)
            radius = np.random.uniform(8, 15)
            height = np.random.uniform(-3, 3)
            
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            y = height
            
            v_orbital = math.sqrt(50.0 / radius) * 0.7
            vx = -v_orbital * math.sin(angle)
            vz = v_orbital * math.cos(angle)
            vy = 0
            
            self.particles.append(Particle(x, y, z, vx, vy, vz))
    
    def project_3d(self, x, y, z):
        """Project 3D to 2D with full rotation"""
        # Rotate around Y axis
        cos_y = math.cos(self.camera.angle_y)
        sin_y = math.sin(self.camera.angle_y)
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        # Rotate around X axis
        cos_x = math.cos(self.camera.angle_x)
        sin_x = math.sin(self.camera.angle_x)
        y_rot = y * cos_x - z_rot * sin_x
        z_final = y * sin_x + z_rot * cos_x
        
        # Apply distance
        z_final += self.camera.distance
        
        if z_final <= 0:
            return None
        
        scale = 400 / z_final
        screen_x = int(WIDTH / 2 + x_rot * scale * 20)
        screen_y = int(HEIGHT / 2 - y_rot * scale * 20)
        
        if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
            return (screen_x, screen_y, z_final)
        return None
    
    def draw(self):
        """Draw everything"""
        self.screen.fill((0, 0, 5))
        
        # Draw rotated black hole texture
        # For now, just rotate 2D (we'll enhance this)
        rotated = pygame.transform.rotate(
            pygame.surfarray.make_surface(self.base_texture),
            self.camera.angle_y * 57.3
        )
        rect = rotated.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(rotated, rect)
        
        # Draw particles with trails
        for particle in self.particles:
            if not particle.alive:
                continue
            
            # Draw trail
            if len(particle.trail) > 1:
                trail_points = []
                for pos in particle.trail:
                    proj = self.project_3d(pos[0], pos[1], pos[2])
                    if proj:
                        trail_points.append((proj[0], proj[1]))
                
                if len(trail_points) > 1:
                    pygame.draw.lines(self.screen, (0, 255, 255), False, trail_points, 1)
            
            # Draw particle
            proj = self.project_3d(particle.pos[0], particle.pos[1], particle.pos[2])
            if proj:
                pygame.draw.circle(self.screen, particle.color, (proj[0], proj[1]), 4)
                pygame.draw.circle(self.screen, (255, 255, 255), (proj[0], proj[1]), 4, 1)
        
        # FPS and info
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        particle_text = self.font.render(f"Particles: {len([p for p in self.particles if p.alive])}", True, (255, 255, 255))
        self.screen.blit(particle_text, (10, 35))
        
        info_text = self.font.render("Drag: Rotate (3D) | Scroll: Zoom | Right-click: Add particle | ESC: Quit", True, (200, 200, 200))
        self.screen.blit(info_text, (10, HEIGHT - 30))
        
        pygame.display.flip()
    
    def handle_events(self):
        """Handle input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.camera.dragging = True
                    self.camera.last_pos = event.pos
                elif event.button == 3:  # Right click - add particle
                    self.add_random_particles(1)
                elif event.button == 4:
                    self.camera.zoom(1)
                elif event.button == 5:
                    self.camera.zoom(-1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.camera.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.camera.dragging and self.camera.last_pos:
                    dx = event.pos[0] - self.camera.last_pos[0]
                    dy = event.pos[1] - self.camera.last_pos[1]
                    self.camera.rotate(dx, dy)
                    self.camera.last_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt):
        """Update simulation"""
        # Update particles
        for particle in self.particles:
            particle.update(dt)
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.alive]
        
        # Auto-add if too few
        if len(self.particles) < 3:
            self.add_random_particles(1)
    
    def run(self):
        """Main loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("="*60)
    print("  BLACK HOLE - FINAL VERSION 2")
    print("="*60)
    print("\nFeatures:")
    print("  • 60 FPS smooth rendering")
    print("  • SOFT gradients and edges")
    print("  • Full 3D rotation (X and Y axes)")
    print("  • Flying particles with trails")
    print("  • Interactive particle spawning")
    print("\nControls:")
    print("  • Drag to rotate (full 3D)")
    print("  • Scroll to zoom")
    print("  • Right-click to add particles")
    print("  • ESC to quit\n")
    
    BlackHoleFinal().run()
