"""
3D Interactive Black Hole Simulation
With mouse controls and realistic physics
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches

# Physical constants
G = 6.67430e-11
C = 299792458
SOLAR_MASS = 1.989e30
BLACK_HOLE_MASS = 10 * SOLAR_MASS
SCHWARZSCHILD_RADIUS = (2 * G * BLACK_HOLE_MASS) / (C ** 2)

# Simulation parameters
SCALE = SCHWARZSCHILD_RADIUS * 1e-6  # Scale for visualization
TIME_STEP = 0.1


class Particle:
    """Particle affected by black hole gravity"""
    
    def __init__(self, pos, vel, mass=1000.0):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.mass = mass
        self.trail = [self.pos.copy()]
        self.alive = True
        
    def update(self, black_hole_pos, black_hole_mass, dt):
        """Update particle position and velocity"""
        if not self.alive:
            return
        
        # Vector from black hole to particle
        r_vec = self.pos - black_hole_pos
        r = np.linalg.norm(r_vec)
        
        # Check if captured
        rs = (2 * G * black_hole_mass) / (C ** 2)
        if r < rs * SCALE:
            self.alive = False
            return
        
        # Gravitational acceleration
        if r > 0:
            accel = -(G * black_hole_mass / r**2) * (r_vec / r)
            
            # Update velocity and position
            self.vel += accel * dt
            self.pos += self.vel * dt
            
            # Store trail
            self.trail.append(self.pos.copy())
            if len(self.trail) > 50:
                self.trail.pop(0)


class BlackHole3DSimulation:
    """3D Interactive Black Hole Simulation"""
    
    def __init__(self):
        self.black_hole_pos = np.array([0.0, 0.0, 0.0])
        self.black_hole_mass = BLACK_HOLE_MASS
        self.particles = []
        
        # Create figure and 3D axis
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set up the plot
        self.setup_plot()
        
        # Mouse interaction
        self.mouse_pressed = False
        self.last_mouse_pos = None
        
        # Connect mouse events
        self.fig.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        
        # Add some initial particles
        self.add_random_particles(5)
        
        # Animation
        self.anim = FuncAnimation(self.fig, self.update, interval=33, blit=False)
        
    def setup_plot(self):
        """Setup the 3D plot"""
        # Set labels
        self.ax.set_xlabel('X (scaled units)', fontsize=10)
        self.ax.set_ylabel('Y (scaled units)', fontsize=10)
        self.ax.set_zlabel('Z (scaled units)', fontsize=10)
        self.ax.set_title('3D Black Hole Simulation\n(Click and drag to rotate, scroll to zoom, right-click to add particles)', 
                         fontsize=12, pad=20)
        
        # Set limits
        limit = 50
        self.ax.set_xlim([-limit, limit])
        self.ax.set_ylim([-limit, limit])
        self.ax.set_zlim([-limit, limit])
        
        # Set background color
        self.ax.set_facecolor('black')
        self.fig.patch.set_facecolor('#1a1a1a')
        
        # Grid
        self.ax.grid(True, alpha=0.3)
        
    def add_random_particles(self, count):
        """Add random particles"""
        for _ in range(count):
            # Random position
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(20, 40)
            height = np.random.uniform(-10, 10)
            
            pos = [
                radius * np.cos(angle),
                height,
                radius * np.sin(angle)
            ]
            
            # Orbital velocity
            r = np.linalg.norm(pos)
            v_orbital = np.sqrt(G * self.black_hole_mass / (r / SCALE)) * SCALE
            
            # Perpendicular velocity
            vel = [
                -v_orbital * np.sin(angle) * 0.8,
                0,
                v_orbital * np.cos(angle) * 0.8
            ]
            
            self.particles.append(Particle(pos, vel))
    
    def add_particle_at_position(self, x, y, z):
        """Add particle at specific position"""
        pos = [x, y, z]
        
        # Calculate orbital velocity
        r = np.linalg.norm(pos)
        if r > 0:
            v_orbital = np.sqrt(G * self.black_hole_mass / (r / SCALE)) * SCALE * 0.7
            
            # Perpendicular direction
            angle = np.arctan2(z, x)
            vel = [
                -v_orbital * np.sin(angle),
                0,
                v_orbital * np.cos(angle)
            ]
        else:
            vel = [0, 0, 0]
        
        self.particles.append(Particle(pos, vel))
    
    def on_mouse_press(self, event):
        """Handle mouse press"""
        if event.button == 3:  # Right click
            # Add particle at clicked location
            if event.inaxes == self.ax:
                # Get 3D coordinates (approximate)
                x = np.random.uniform(-30, 30)
                y = np.random.uniform(-30, 30)
                z = np.random.uniform(-30, 30)
                self.add_particle_at_position(x, y, z)
        else:
            self.mouse_pressed = True
            self.last_mouse_pos = (event.x, event.y)
    
    def on_mouse_release(self, event):
        """Handle mouse release"""
        self.mouse_pressed = False
    
    def on_mouse_move(self, event):
        """Handle mouse movement for rotation"""
        if self.mouse_pressed and self.last_mouse_pos and event.inaxes == self.ax:
            dx = event.x - self.last_mouse_pos[0]
            dy = event.y - self.last_mouse_pos[1]
            
            # Rotate view
            self.ax.view_init(elev=self.ax.elev + dy * 0.5, azim=self.ax.azim - dx * 0.5)
            self.last_mouse_pos = (event.x, event.y)
            self.fig.canvas.draw_idle()
    
    def on_scroll(self, event):
        """Handle scroll for zoom"""
        # Get current limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        zlim = self.ax.get_zlim()
        
        # Zoom factor
        zoom_factor = 1.1 if event.button == 'down' else 0.9
        
        # Calculate new limits
        x_range = (xlim[1] - xlim[0]) * zoom_factor / 2
        y_range = (ylim[1] - ylim[0]) * zoom_factor / 2
        z_range = (zlim[1] - zlim[0]) * zoom_factor / 2
        
        # Set new limits
        self.ax.set_xlim([-x_range, x_range])
        self.ax.set_ylim([-y_range, y_range])
        self.ax.set_zlim([-z_range, z_range])
        
        self.fig.canvas.draw_idle()
    
    def update(self, frame):
        """Update simulation"""
        # Clear axis
        self.ax.clear()
        self.setup_plot()
        
        # Update particles
        for particle in self.particles:
            particle.update(self.black_hole_pos, self.black_hole_mass, TIME_STEP)
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.alive]
        
        # Draw black hole (event horizon)
        rs_scaled = (2 * G * self.black_hole_mass) / (C ** 2) * SCALE
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        x = rs_scaled * np.outer(np.cos(u), np.sin(v))
        y = rs_scaled * np.outer(np.sin(u), np.sin(v))
        z = rs_scaled * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax.plot_surface(x, y, z, color='black', alpha=0.9, edgecolor='red', linewidth=0.5)
        
        # Draw photon sphere
        ps_radius = rs_scaled * 1.5
        x_ps = ps_radius * np.outer(np.cos(u), np.sin(v))
        y_ps = ps_radius * np.outer(np.sin(u), np.sin(v))
        z_ps = ps_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax.plot_surface(x_ps, y_ps, z_ps, color='yellow', alpha=0.1, edgecolor='yellow', linewidth=0.3)
        
        # Draw particles and trails
        for particle in self.particles:
            if len(particle.trail) > 1:
                trail = np.array(particle.trail)
                self.ax.plot(trail[:, 0], trail[:, 1], trail[:, 2], 
                           color='cyan', alpha=0.5, linewidth=1)
            
            # Draw particle
            self.ax.scatter(particle.pos[0], particle.pos[1], particle.pos[2],
                          color='lime', s=50, marker='o', edgecolors='white', linewidth=0.5)
        
        # Add info text
        info_text = f"Particles: {len(self.particles)}\n"
        info_text += f"Black Hole Mass: {self.black_hole_mass/SOLAR_MASS:.1f} M☉\n"
        info_text += f"Schwarzschild Radius: {SCHWARZSCHILD_RADIUS:.2f} m\n"
        info_text += "\nControls:\n"
        info_text += "• Left-click + drag: Rotate\n"
        info_text += "• Scroll: Zoom\n"
        info_text += "• Right-click: Add particle"
        
        self.ax.text2D(0.02, 0.98, info_text, transform=self.ax.transAxes,
                      fontsize=9, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='black', alpha=0.7),
                      color='white', family='monospace')
        
        return self.ax,
    
    def run(self):
        """Run the simulation"""
        plt.show()


def main():
    """Main entry point"""
    print("="*60)
    print("  3D INTERACTIVE BLACK HOLE SIMULATION")
    print("="*60)
    print("\nStarting 3D visualization...")
    print("\nControls:")
    print("  • Left-click and drag to rotate the view")
    print("  • Scroll to zoom in/out")
    print("  • Right-click to add particles")
    print("  • Close window to exit")
    print("\nLaunching...\n")
    
    sim = BlackHole3DSimulation()
    sim.run()


if __name__ == "__main__":
    main()
