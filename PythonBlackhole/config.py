"""
Configuration file for Black Hole Simulation
Contains physical constants and simulation parameters
"""

import math

# Physical Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
C = 299792458    # Speed of light (m/s)
H = 6.62607015e-34  # Planck constant (J⋅s)
K_B = 1.380649e-23  # Boltzmann constant (J/K)
SIGMA = 5.670374419e-8  # Stefan-Boltzmann constant (W⋅m^-2⋅K^-4)

# Black Hole Parameters
SOLAR_MASS = 1.989e30  # kg
BLACK_HOLE_MASS = 10 * SOLAR_MASS  # 10 solar masses
SCHWARZSCHILD_RADIUS = (2 * G * BLACK_HOLE_MASS) / (C ** 2)  # meters

# Simulation Parameters
SIMULATION_SCALE = 1e-6  # Scale factor for visualization (1 unit = 1 million meters)
TIME_STEP = 0.1  # seconds per frame
SIMULATION_SPEED = 1.0  # Speed multiplier
MAX_PARTICLES = 100  # Maximum number of particles

# Display Settings
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 40
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
ZOOM_LEVEL = 1.0

# Visualization ranges (in scaled units)
VIEW_RANGE = 50  # Range of view in simulation units

# Color codes (using ANSI escape sequences)
COLOR_BLACK_HOLE = '\033[95m'  # Magenta for black hole
COLOR_EVENT_HORIZON = '\033[91m'  # Red for event horizon
COLOR_PHOTON_SPHERE = '\033[93m'  # Yellow for photon sphere
COLOR_ACCRETION_DISK = '\033[96m'  # Cyan for accretion disk
COLOR_PARTICLE = '\033[92m'  # Green for particles
COLOR_PARTICLE_HOT = '\033[91m'  # Red for hot particles
COLOR_PARTICLE_COLD = '\033[94m'  # Blue for cold particles
COLOR_INFO = '\033[97m'  # White for info text
COLOR_WARNING = '\033[93m'  # Yellow for warnings
COLOR_RESET = '\033[0m'  # Reset color

# Physics zones (in Schwarzschild radii)
EVENT_HORIZON_RADIUS = 1.0  # 1 Rs
PHOTON_SPHERE_RADIUS = 1.5  # 1.5 Rs
ISCO_RADIUS = 3.0  # Innermost Stable Circular Orbit (3 Rs for non-rotating)
SAFE_ZONE_RADIUS = 10.0  # 10 Rs

# Accretion Disk Parameters
ACCRETION_RATE = 1e-8  # Mass accretion rate (solar masses per year)
DISK_INNER_RADIUS = ISCO_RADIUS
DISK_OUTER_RADIUS = 20.0  # In Schwarzschild radii
DISK_TEMPERATURE_INNER = 1e7  # Kelvin
DISK_TEMPERATURE_OUTER = 1e4  # Kelvin

# Particle Generation
PARTICLE_SPAWN_RATE = 0.1  # Probability per frame
PARTICLE_INITIAL_DISTANCE_MIN = 15.0  # In Schwarzschild radii
PARTICLE_INITIAL_DISTANCE_MAX = 40.0
PARTICLE_INITIAL_VELOCITY_RANGE = 1000.0  # m/s

# Rendering
FRAME_RATE = 30  # Target frames per second
TRAIL_LENGTH = 20  # Number of previous positions to show

# Unicode characters for rendering
CHAR_BLACK_HOLE = '●'
CHAR_EVENT_HORIZON = '◉'
CHAR_PARTICLE = '•'
CHAR_PARTICLE_TRAIL = '·'
CHAR_ACCRETION = '~'
CHAR_EMPTY = ' '
CHAR_GRID = '·'
