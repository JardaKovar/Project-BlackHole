"""
Utility functions for the Black Hole Simulation
Mathematical helpers, vector operations, and conversions
"""

import math
import numpy as np
from config import *


class Vector3D:
    """3D Vector class for position and velocity calculations"""
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def magnitude(self):
        """Calculate the magnitude of the vector"""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        """Return a normalized version of the vector"""
        mag = self.magnitude()
        if mag > 0:
            return self / mag
        return Vector3D(0, 0, 0)
    
    def dot(self, other):
        """Dot product with another vector"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        """Cross product with another vector"""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def copy(self):
        """Return a copy of the vector"""
        return Vector3D(self.x, self.y, self.z)
    
    def __repr__(self):
        return f"Vector3D({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


def calculate_schwarzschild_radius(mass):
    """Calculate the Schwarzschild radius for a given mass"""
    return (2 * G * mass) / (C ** 2)


def calculate_escape_velocity(mass, distance):
    """Calculate escape velocity at a given distance from the black hole"""
    if distance <= 0:
        return 0
    return math.sqrt((2 * G * mass) / distance)


def calculate_orbital_velocity(mass, distance):
    """Calculate orbital velocity for a circular orbit at given distance"""
    if distance <= 0:
        return 0
    return math.sqrt((G * mass) / distance)


def calculate_time_dilation(distance, mass):
    """
    Calculate gravitational time dilation factor
    Returns the ratio of proper time to coordinate time
    """
    rs = calculate_schwarzschild_radius(mass)
    if distance <= rs:
        return 0  # Time stops at event horizon
    return math.sqrt(1 - rs / distance)


def calculate_gravitational_redshift(distance, mass):
    """Calculate gravitational redshift factor"""
    rs = calculate_schwarzschild_radius(mass)
    if distance <= rs:
        return float('inf')
    return 1 / math.sqrt(1 - rs / distance)


def calculate_tidal_force(mass, distance, object_length):
    """
    Calculate tidal force (spaghettification effect)
    Returns the difference in gravitational acceleration across the object
    """
    if distance <= 0:
        return 0
    
    # Acceleration at near end
    a_near = (G * mass) / (distance - object_length/2)**2
    # Acceleration at far end
    a_far = (G * mass) / (distance + object_length/2)**2
    
    return abs(a_near - a_far)


def calculate_hawking_temperature(mass):
    """Calculate Hawking temperature of the black hole"""
    rs = calculate_schwarzschild_radius(mass)
    return (H * C**3) / (8 * math.pi * K_B * G * mass)


def calculate_hawking_luminosity(mass):
    """Calculate Hawking radiation luminosity"""
    temp = calculate_hawking_temperature(mass)
    rs = calculate_schwarzschild_radius(mass)
    area = 4 * math.pi * rs**2
    return SIGMA * area * temp**4


def calculate_black_hole_lifetime(mass):
    """Calculate evaporation time due to Hawking radiation (in years)"""
    # Lifetime in seconds
    lifetime_seconds = (5120 * math.pi * G**2 * mass**3) / (H * C**4)
    # Convert to years
    return lifetime_seconds / (365.25 * 24 * 3600)


def calculate_accretion_disk_temperature(radius_rs, mass):
    """
    Calculate temperature of accretion disk at given radius
    radius_rs: radius in Schwarzschild radii
    """
    rs = calculate_schwarzschild_radius(mass)
    radius = radius_rs * rs
    
    # Simplified temperature profile (decreases with radius)
    if radius_rs < DISK_INNER_RADIUS:
        return DISK_TEMPERATURE_INNER
    elif radius_rs > DISK_OUTER_RADIUS:
        return DISK_TEMPERATURE_OUTER
    
    # Power-law temperature profile
    temp = DISK_TEMPERATURE_INNER * (radius_rs / DISK_INNER_RADIUS)**(-0.75)
    return max(temp, DISK_TEMPERATURE_OUTER)


def meters_to_schwarzschild_radii(distance_meters, mass):
    """Convert distance in meters to Schwarzschild radii"""
    rs = calculate_schwarzschild_radius(mass)
    return distance_meters / rs


def schwarzschild_radii_to_meters(distance_rs, mass):
    """Convert distance in Schwarzschild radii to meters"""
    rs = calculate_schwarzschild_radius(mass)
    return distance_rs * rs


def format_scientific(value, precision=2):
    """Format a number in scientific notation"""
    if value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value))))
    mantissa = value / (10 ** exponent)
    return f"{mantissa:.{precision}f}e{exponent:+d}"


def format_distance(distance_meters):
    """Format distance with appropriate units"""
    if distance_meters < 1000:
        return f"{distance_meters:.2f} m"
    elif distance_meters < 1e6:
        return f"{distance_meters/1e3:.2f} km"
    elif distance_meters < 1e9:
        return f"{distance_meters/1e6:.2f} Mm"
    else:
        return f"{distance_meters/1e9:.2f} Gm"


def format_mass(mass_kg):
    """Format mass in terms of solar masses"""
    solar_masses = mass_kg / SOLAR_MASS
    return f"{solar_masses:.2f} M☉"


def format_temperature(temp_kelvin):
    """Format temperature with appropriate units"""
    if temp_kelvin < 1e3:
        return f"{temp_kelvin:.2f} K"
    elif temp_kelvin < 1e6:
        return f"{temp_kelvin/1e3:.2f} kK"
    elif temp_kelvin < 1e9:
        return f"{temp_kelvin/1e6:.2f} MK"
    else:
        return f"{temp_kelvin/1e9:.2f} GK"


def clamp(value, min_value, max_value):
    """Clamp a value between min and max"""
    return max(min_value, min(max_value, value))


def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t


def rotate_point_2d(x, y, angle):
    """Rotate a 2D point around the origin"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)


def project_3d_to_2d(pos_3d, camera_distance=100):
    """
    Simple perspective projection from 3D to 2D
    Returns (x, y) screen coordinates
    """
    if pos_3d.z + camera_distance == 0:
        return (pos_3d.x, pos_3d.y)
    
    scale = camera_distance / (pos_3d.z + camera_distance)
    return (pos_3d.x * scale, pos_3d.y * scale)


def get_color_from_temperature(temp_kelvin):
    """Get color code based on temperature"""
    if temp_kelvin > 1e7:
        return COLOR_PARTICLE_HOT
    elif temp_kelvin > 1e5:
        return '\033[91m'  # Red
    elif temp_kelvin > 1e4:
        return '\033[93m'  # Yellow
    elif temp_kelvin > 1e3:
        return '\033[96m'  # Cyan
    else:
        return COLOR_PARTICLE_COLD


def calculate_relativistic_factor(velocity):
    """Calculate Lorentz factor (gamma) for relativistic effects"""
    v_ratio = velocity / C
    if v_ratio >= 1:
        return float('inf')
    return 1 / math.sqrt(1 - v_ratio**2)
