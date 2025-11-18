"""
Black Hole Simulation - Main Program
A super detailed black hole simulation with realistic physics
"""

import sys
import time
import math
import random
import threading
from config import *
from utils import *
from black_hole_physics import BlackHole, AccretionDisk
from particle_system import ParticleSystem
from visualization import Renderer

# Initialize colorama for Windows
try:
    import colorama
    colorama.init(autoreset=False, strip=False)
except ImportError:
    pass

# Try to import keyboard for input handling
try:
    import msvcrt  # Windows
    WINDOWS = True
except ImportError:
    import tty
    import termios
    WINDOWS = False


class BlackHoleSimulation:
    """Main simulation class"""
    
    def __init__(self):
        # Initialize components
        self.black_hole = BlackHole(BLACK_HOLE_MASS)
        self.particle_system = ParticleSystem(self.black_hole)
        self.accretion_disk = AccretionDisk(self.black_hole, num_particles=30)
        self.renderer = Renderer()
        
        # Simulation state
        self.running = False
        self.paused = False
        self.simulation_time = 0.0
        self.frame_count = 0
        self.fps = 0.0
        self.last_fps_update = time.time()
        self.fps_frame_count = 0
        
        # Time control
        self.time_step = TIME_STEP
        self.speed_multiplier = SIMULATION_SPEED
        
        # Auto-spawn particles
        self.auto_spawn = True
        self.spawn_timer = 0.0
        self.spawn_interval = 2.0  # seconds
        
        # Input handling
        self.input_thread = None
        self.last_key = None
        
    def initialize(self):
        """Initialize the simulation"""
        print(f"{COLOR_INFO}Initializing Black Hole Simulation...{COLOR_RESET}")
        print(f"Black Hole Mass: {format_mass(self.black_hole.mass)}")
        print(f"Schwarzschild Radius: {format_distance(self.black_hole.schwarzschild_radius)}")
        print(f"Event Horizon: {format_distance(self.black_hole.event_horizon_radius)}")
        print(f"Photon Sphere: {format_distance(self.black_hole.photon_sphere_radius)}")
        print(f"ISCO: {format_distance(self.black_hole.isco_radius)}")
        print(f"\n{COLOR_WARNING}Press any key to start...{COLOR_RESET}")
        
        # Wait for key press
        self.wait_for_key()
        
        # Add initial particles
        for _ in range(5):
            self.particle_system.add_particle()
        
        print(f"\n{COLOR_INFO}Simulation started!{COLOR_RESET}")
        time.sleep(1)
    
    def wait_for_key(self):
        """Wait for a key press"""
        if WINDOWS:
            msvcrt.getch()
        else:
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def get_key_non_blocking(self):
        """Get key press without blocking (returns None if no key pressed)"""
        if WINDOWS:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    return key.decode('utf-8').lower()
                except:
                    return None
        else:
            # Unix-like systems - non-blocking input is complex
            # For simplicity, we'll skip non-blocking input on Unix
            return None
        return None
    
    def handle_input(self):
        """Handle user input"""
        key = self.get_key_non_blocking()
        
        if key:
            if key == 'q':
                self.running = False
            elif key == ' ':
                # Add particle
                self.particle_system.add_particle()
            elif key == 'p':
                # Pause/unpause
                self.paused = not self.paused
            elif key == 'v':
                # Change view mode
                self.renderer.toggle_view_mode()
            elif key == '+' or key == '=':
                # Zoom in
                self.renderer.zoom_in()
            elif key == '-' or key == '_':
                # Zoom out
                self.renderer.zoom_out()
            elif key == 'g':
                # Toggle grid
                self.renderer.toggle_grid()
            elif key == 't':
                # Toggle trails
                self.renderer.toggle_trails()
            elif key == 'a':
                # Toggle accretion disk
                self.renderer.toggle_accretion_disk()
            elif key == 'c':
                # Clear all particles
                self.particle_system.clear_all()
            elif key == 's':
                # Toggle auto-spawn
                self.auto_spawn = not self.auto_spawn
            elif key == '[':
                # Slow down
                self.speed_multiplier = max(0.1, self.speed_multiplier * 0.5)
            elif key == ']':
                # Speed up
                self.speed_multiplier = min(10.0, self.speed_multiplier * 2.0)
            elif key == 'r':
                # Reset simulation
                self.reset()
    
    def reset(self):
        """Reset the simulation"""
        self.particle_system.clear_all()
        self.simulation_time = 0.0
        self.frame_count = 0
        
        # Reinitialize black hole
        self.black_hole = BlackHole(BLACK_HOLE_MASS)
        self.particle_system.black_hole = self.black_hole
        self.accretion_disk = AccretionDisk(self.black_hole, num_particles=30)
        
        # Add initial particles
        for _ in range(5):
            self.particle_system.add_particle()
    
    def update(self, dt):
        """Update simulation state"""
        if self.paused:
            return
        
        # Apply speed multiplier
        effective_dt = dt * self.speed_multiplier
        
        # Update black hole (Hawking radiation)
        self.black_hole.apply_hawking_radiation(effective_dt)
        
        # Update accretion disk
        self.accretion_disk.update(effective_dt)
        
        # Update particles
        self.particle_system.update(effective_dt)
        
        # Auto-spawn particles
        if self.auto_spawn:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0.0
                if len(self.particle_system.get_active_particles()) < MAX_PARTICLES:
                    self.particle_system.add_particle()
        
        # Update simulation time
        self.simulation_time += effective_dt
        self.frame_count += 1
    
    def render(self):
        """Render the simulation"""
        # Clear buffer
        self.renderer.clear_buffer()
        
        # Render grid
        self.renderer.render_grid()
        
        # Render accretion disk
        self.renderer.render_accretion_disk(self.accretion_disk)
        
        # Render black hole
        self.renderer.render_black_hole(self.black_hole)
        
        # Render particles
        self.renderer.render_particles(self.particle_system)
        
        # Render info panel
        info_lines = self.renderer.render_info_panel(
            self.black_hole,
            self.particle_system,
            self.simulation_time,
            self.fps
        )
        
        # Display
        self.renderer.display(info_lines)
        
        # Update FPS
        self.fps_frame_count += 1
        current_time = time.time()
        if current_time - self.last_fps_update >= 1.0:
            self.fps = self.fps_frame_count / (current_time - self.last_fps_update)
            self.fps_frame_count = 0
            self.last_fps_update = current_time
    
    def run(self):
        """Main simulation loop"""
        self.running = True
        last_time = time.time()
        target_frame_time = 1.0 / FRAME_RATE
        
        try:
            while self.running:
                current_time = time.time()
                dt = current_time - last_time
                last_time = current_time
                
                # Handle input
                self.handle_input()
                
                # Update simulation
                self.update(dt)
                
                # Render
                self.render()
                
                # Frame rate limiting
                frame_time = time.time() - current_time
                if frame_time < target_frame_time:
                    time.sleep(target_frame_time - frame_time)
        
        except KeyboardInterrupt:
            print(f"\n{COLOR_INFO}Simulation interrupted by user.{COLOR_RESET}")
        except Exception as e:
            print(f"\n{COLOR_WARNING}Error: {e}{COLOR_RESET}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up and show final statistics"""
        print(f"\n{COLOR_INFO}╔═══════════════════════════════════════╗{COLOR_RESET}")
        print(f"{COLOR_INFO}║     SIMULATION STATISTICS             ║{COLOR_RESET}")
        print(f"{COLOR_INFO}╚═══════════════════════════════════════╝{COLOR_RESET}")
        
        stats = self.particle_system.get_statistics()
        
        print(f"\n{COLOR_INFO}Black Hole:{COLOR_RESET}")
        print(f"  Final Mass: {format_mass(self.black_hole.mass)}")
        print(f"  Mass Accreted: {format_scientific(self.black_hole.accreted_mass)} kg")
        print(f"  Energy Radiated: {format_scientific(self.black_hole.total_energy_radiated)} J")
        
        print(f"\n{COLOR_INFO}Particles:{COLOR_RESET}")
        print(f"  Total Created: {stats['total_created']}")
        print(f"  Captured by Black Hole: {stats['captured']}")
        print(f"  Escaped: {stats['escaped']}")
        print(f"  Final Active: {stats['active']}")
        
        print(f"\n{COLOR_INFO}Simulation:{COLOR_RESET}")
        print(f"  Total Time: {self.simulation_time:.2f} seconds")
        print(f"  Total Frames: {self.frame_count}")
        print(f"  Average FPS: {self.frame_count / (time.time() - self.last_fps_update + 1):.2f}")
        
        print(f"\n{COLOR_INFO}Thank you for using Black Hole Simulation!{COLOR_RESET}\n")


def print_welcome():
    """Print welcome message"""
    print(f"{COLOR_BLACK_HOLE}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                                                               ║")
    print("║           ★  BLACK HOLE SIMULATION  ★                        ║")
    print("║                                                               ║")
    print("║         A Super Detailed Physics Simulation                  ║")
    print("║                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{COLOR_RESET}")
    print(f"\n{COLOR_INFO}Features:{COLOR_RESET}")
    print("  • Realistic gravitational physics")
    print("  • Event horizon and photon sphere")
    print("  • Accretion disk with temperature gradients")
    print("  • Particle trajectories and orbital mechanics")
    print("  • Time dilation effects")
    print("  • Hawking radiation")
    print("  • Spaghettification (tidal forces)")
    print("  • Multiple view modes")
    print("  • Real-time statistics")
    
    print(f"\n{COLOR_WARNING}Controls:{COLOR_RESET}")
    print("  SPACE    - Add particle")
    print("  P        - Pause/Resume")
    print("  V        - Change view mode (Top/Side/3D)")
    print("  +/-      - Zoom in/out")
    print("  [/]      - Slow down/Speed up")
    print("  G        - Toggle grid")
    print("  T        - Toggle particle trails")
    print("  A        - Toggle accretion disk")
    print("  S        - Toggle auto-spawn particles")
    print("  C        - Clear all particles")
    print("  R        - Reset simulation")
    print("  Q        - Quit")
    
    print(f"\n{COLOR_INFO}Physics Information:{COLOR_RESET}")
    print(f"  Gravitational Constant: {format_scientific(G)} m³ kg⁻¹ s⁻²")
    print(f"  Speed of Light: {format_scientific(C)} m/s")
    print(f"  Black Hole Mass: {format_mass(BLACK_HOLE_MASS)}")
    print(f"  Schwarzschild Radius: {format_distance(SCHWARZSCHILD_RADIUS)}")
    print()


def main():
    """Main entry point"""
    try:
        # Print welcome message
        print_welcome()
        
        # Create and initialize simulation
        sim = BlackHoleSimulation()
        sim.initialize()
        
        # Run simulation
        sim.run()
        
    except Exception as e:
        print(f"\n{COLOR_WARNING}Fatal Error: {e}{COLOR_RESET}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
