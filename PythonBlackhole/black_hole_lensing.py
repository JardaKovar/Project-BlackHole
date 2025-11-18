"""
Black Hole Gravitational Lensing Visualization
Shows realistic black hole with light bending effects
"""

import sys
import time
import os
from config import *
from utils import *
from black_hole_physics import BlackHole
from particle_system import ParticleSystem
from lensing_renderer import LensingRenderer

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
    WINDOWS = False


class BlackHoleLensingSimulation:
    """Main simulation with gravitational lensing visualization"""
    
    def __init__(self):
        self.black_hole = BlackHole(BLACK_HOLE_MASS)
        self.particle_system = ParticleSystem(self.black_hole)
        self.renderer = LensingRenderer(width=120, height=40)
        
        # Simulation state
        self.running = False
        self.simulation_time = 0.0
        self.fps = 0.0
        self.last_fps_update = time.time()
        self.fps_frame_count = 0
        
        # Add some initial particles
        for _ in range(3):
            self.particle_system.add_particle()
    
    def clear_screen(self):
        """Clear the terminal screen"""
        if os.name == 'nt':
            os.system('cls')
        else:
            print('\033[2J\033[H', end='')
    
    def get_key_non_blocking(self):
        """Get key press without blocking"""
        if WINDOWS:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    return key.decode('utf-8').lower()
                except:
                    return None
        return None
    
    def handle_input(self):
        """Handle user input"""
        key = self.get_key_non_blocking()
        
        if key:
            if key == 'q':
                self.running = False
            elif key == ' ':
                self.particle_system.add_particle()
            elif key == 'c':
                self.particle_system.clear_all()
    
    def update(self, dt):
        """Update simulation"""
        self.particle_system.update(dt)
        self.simulation_time += dt
    
    def render(self):
        """Render the visualization"""
        self.clear_screen()
        
        particle_count = len(self.particle_system.get_active_particles())
        output = self.renderer.render_with_info(
            self.black_hole,
            self.simulation_time,
            self.fps,
            particle_count
        )
        
        print(output, flush=True)
        
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
        target_frame_time = 1.0 / 30  # 30 FPS
        
        # Initial render
        self.render()
        time.sleep(1)
        
        try:
            while self.running:
                current_time = time.time()
                dt = current_time - last_time
                last_time = current_time
                
                self.handle_input()
                self.update(dt)
                self.render()
                
                # Frame rate limiting
                frame_time = time.time() - current_time
                if frame_time < target_frame_time:
                    time.sleep(target_frame_time - frame_time)
        
        except KeyboardInterrupt:
            print("\n\nSimulation interrupted by user.")
        except Exception as e:
            print(f"\n\nError: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up"""
        stats = self.particle_system.get_statistics()
        print(f"\n\nSimulation Statistics:")
        print(f"  Total Particles Created: {stats['total_created']}")
        print(f"  Captured by Black Hole: {stats['captured']}")
        print(f"  Escaped: {stats['escaped']}")
        print(f"  Total Time: {self.simulation_time:.2f} seconds")
        print(f"\nThank you for exploring the black hole!\n")


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("  BLACK HOLE GRAVITATIONAL LENSING VISUALIZATION")
    print("="*60)
    print("\nThis simulation shows a realistic black hole with:")
    print("  • Gravitational lensing (light bending)")
    print("  • Photon ring (bright yellow ring)")
    print("  • Accretion disk (orange/red disk)")
    print("  • Doppler boosting (one side brighter)")
    print("  • Event horizon (black center)")
    print("\nBased on General Relativity and the Schwarzschild metric")
    print("\nControls:")
    print("  SPACE - Add particle")
    print("  C     - Clear particles")
    print("  Q     - Quit")
    print("\nPress any key to start...")
    
    if WINDOWS:
        msvcrt.getch()
    else:
        input()


def main():
    """Main entry point"""
    try:
        print_welcome()
        
        sim = BlackHoleLensingSimulation()
        sim.run()
        
    except Exception as e:
        print(f"\nFatal Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
