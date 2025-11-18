"""
Perfect Black Hole Visualization
Full 3D rotation with proper particle physics
"""

import pygame
import numpy as np
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

class Camera:
    """3D Camera"""
    
    def __init__(self):
        self.angle_x = 0.3
        self.angle_y = 0.0
        self.distance = 150
        self.dragging = False
        self.last_pos = None
    
    def rotate(self, dx, dy):
        """Rotate camera"""
        self.angle_y += dx * 0.005
        self.angle_x += dy * 0.005
        self.angle_x = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.angle_x))
    
    def zoom(self, amount):
        """Zoom"""
        self.distance *= (0.9 if amount > 0 else 1.1)
        self.distance = max(80, min(250, self.distance))
    
    def project(self, x, y, z):
        """Project 3D to 2D"""
        # Rotate Y
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        # Rotate X
        cos_x = math.cos(self.angle_x)
        sin_x = math.sin(self.angle_x)
        y_rot = y * cos_x - z_rot * sin_x
        z_final = y * sin_x + z_rot * cos_x
        
        # Distance
        z_final += self.distance
        
        if z_final <= 0:
            return None
        
        scale = 500 / z_final
        screen_x = int(WIDTH / 2 + x_rot * scale)
        screen_y = int(HEIGHT / 2 - y_rot * scale)
        
        return (screen_x, screen_y, z_final)


class Particle:
    """Particle with proper physics"""
    
    def __init__(self, x, y, z, vx, vy, vz):
        self.pos = np.array([x, y, z], dtype=float)
        self.vel = np.array([vx, vy, vz], dtype=float)
        self.trail = []
        self.alive = True
        self.color = (0, 255, 0)
    
    def update(self, dt):
        """Update particle"""
        if not self.alive:
            return
        
        r = np.linalg.norm(self.pos)
        
        # Captured
        if r < 5:
            self.alive = False
            return
        
        # Escaped
        if r > 200:
            self.alive = False
            return
        
        # Gravity
        if r > 0:
            accel = -100.0 * self.pos / (r ** 2)
            self.vel += accel * dt
            self.pos += self.vel * dt
            
            # Trail
            self.trail.append(self.pos.copy())
            if len(self.trail) > 30:
                self.trail.pop(0)
            
            # Color by speed
            speed = np.linalg.norm(self.vel)
            if speed > 20:
                self.color = (255, 0, 0)
            elif speed > 10:
                self.color = (255, 165, 0)
            else:
                self.color = (0, 255, 0)


class BlackHolePerfect:
    """Perfect black hole with full 3D"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Black Hole - Perfect 3D")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.camera = Camera()
        self.particles = []
        self.running = True
        self.paused = False
        
        # Add particles
        self.add_random_particles(8)
        
        print("Ready! Full 3D rotation enabled.")
    
    def add_random_particles(self, count):
        """Add particles"""
        for _ in range(count):
            angle = np.random.uniform(0, 2 * math.pi)
            radius = np.random.uniform(40, 80)
            height = np.random.uniform(-20, 20)
            
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            y = height
            
            v_orbital = math.sqrt(100.0 / radius) * 0.8
            vx = -v_orbital * math.sin(angle)
            vz = v_orbital * math.cos(angle)
            vy = 0
            
            self.particles.append(Particle(x, y, z, vx, vy, vz))
    
    def draw_accretion_disk_3d(self):
        """Draw 3D accretion disk"""
        rotation = pygame.time.get_ticks() * 0.0002
        
        disk_particles = []
        
        for ring_radius in range(10, 40, 2):
            segments = 40
            
            for i in range(segments):
                angle = (i / segments) * 2 * math.pi + rotation
                
                x = ring_radius * math.cos(angle)
                z = ring_radius * math.sin(angle)
                y = np.random.normal(0, 0.3)
                
                proj = self.camera.project(x, y, z)
                if proj:
                    # Color by temperature
                    temp = 1.0 - (ring_radius - 10) / 30
                    
                    if temp > 0.7:
                        color = (255, 255, int(220 * temp))
                    elif temp > 0.4:
                        color = (255, int(200 * temp), int(50 * temp))
                    else:
                        color = (int(255 * temp), int(80 * temp), 0)
                    
                    disk_particles.append((proj[0], proj[1], proj[2], color))
        
        # Sort by depth
        disk_particles.sort(key=lambda p: -p[2])
        
        # Draw
        for px, py, _, color in disk_particles:
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                pygame.draw.circle(self.screen, color, (px, py), 2)
    
    def draw_black_hole_sphere(self):
        """Draw 3D black hole sphere"""
        segments = 20
        points = []
        
        for i in range(segments):
            lat = (i / segments) * math.pi
            for j in range(segments * 2):
                lon = (j / (segments * 2)) * 2 * math.pi
                
                x = 5 * math.sin(lat) * math.cos(lon)
                y = 5 * math.cos(lat)
                z = 5 * math.sin(lat) * math.sin(lon)
                
                proj = self.camera.project(x, y, z)
                if proj:
                    points.append((proj[0], proj[1], proj[2]))
        
        # Sort and draw
        points.sort(key=lambda p: -p[2])
        for px, py, _ in points:
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                pygame.draw.circle(self.screen, (0, 0, 0), (px, py), 3)
    
    def draw_glow_rings(self):
        """Draw glow rings around black hole"""
        for glow_radius in [7, 9, 11]:
            segments = 50
            points = []
            
            for i in range(segments + 1):
                angle = (i / segments) * 2 * math.pi
                x = glow_radius * math.cos(angle)
                z = glow_radius * math.sin(angle)
                y = 0
                
                proj = self.camera.project(x, y, z)
                if proj:
                    points.append((proj[0], proj[1]))
            
            if len(points) > 2:
                alpha = int(100 * (1 - (glow_radius - 7) / 4))
                color = (255, alpha, 0)
                pygame.draw.lines(self.screen, color, False, points, 2)
    
    def draw(self):
        """Draw everything"""
        self.screen.fill((0, 0, 5))
        
        # Draw accretion disk (behind)
        self.draw_accretion_disk_3d()
        
        # Draw glow
        self.draw_glow_rings()
        
        # Draw black hole
        self.draw_black_hole_sphere()
        
        # Draw particles
        for particle in self.particles:
            if not particle.alive:
                continue
            
            # Trail
            if len(particle.trail) > 1:
                trail_points = []
                for pos in particle.trail:
                    proj = self.camera.project(pos[0], pos[1], pos[2])
                    if proj:
                        trail_points.append((proj[0], proj[1]))
                
                if len(trail_points) > 1:
                    pygame.draw.lines(self.screen, (0, 255, 255), False, trail_points, 1)
            
            # Particle
            proj = self.camera.project(particle.pos[0], particle.pos[1], particle.pos[2])
            if proj:
                pygame.draw.circle(self.screen, particle.color, (proj[0], proj[1]), 4)
                pygame.draw.circle(self.screen, (255, 255, 255), (proj[0], proj[1]), 4, 1)
        
        # Info
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        particle_text = self.font.render(f"Particles: {len([p for p in self.particles if p.alive])}", True, (255, 255, 255))
        self.screen.blit(particle_text, (10, 35))
        
        if self.paused:
            pause_text = self.font.render("PAUSED", True, (255, 255, 0))
            self.screen.blit(pause_text, (WIDTH//2 - 40, 10))
        
        info_text = self.font.render("Drag: Rotate 3D | Scroll: Zoom | Right-click: Add | SPACE: Pause | ESC: Quit", True, (200, 200, 200))
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
                elif event.button == 3:
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
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
    
    def update(self, dt):
        """Update"""
        if self.paused:
            return
        
        for particle in self.particles:
            particle.update(dt)
        
        self.particles = [p for p in self.particles if p.alive]
        
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
    print("  BLACK HOLE - PERFECT 3D VERSION")
    print("="*60)
    print("\nFeatures:")
    print("  • TRUE 3D rotation (all axes)")
    print("  • Fixed particle physics")
    print("  • Smooth cyan trails")
    print("  • 3D accretion disk")
    print("  • 60 FPS performance")
    print("\nControls:")
    print("  • Drag to rotate (FULL 3D)")
    print("  • Scroll to zoom")
    print("  • Right-click to add particles")
    print("  • SPACE to pause")
    print("  • ESC to quit\n")
    
    BlackHolePerfect().run()
