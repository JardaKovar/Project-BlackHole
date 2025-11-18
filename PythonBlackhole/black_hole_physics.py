"""
Black Hole Physics Module
Handles all physics calculations for the black hole simulation
"""

import math
import numpy as np
from config import *
from utils import *


class BlackHole:
    """Represents a black hole with all its physical properties"""
    
    def __init__(self, mass=BLACK_HOLE_MASS, position=None):
        self.mass = mass
        self.position = position if position else Vector3D(0, 0, 0)
        
        # Calculate derived properties
        self.schwarzschild_radius = calculate_schwarzschild_radius(mass)
        self.event_horizon_radius = self.schwarzschild_radius
        self.photon_sphere_radius = 1.5 * self.schwarzschild_radius
        self.isco_radius = 3.0 * self.schwarzschild_radius
        
        # Hawking radiation properties
        self.temperature = calculate_hawking_temperature(mass)
        self.luminosity = calculate_hawking_luminosity(mass)
        self.lifetime = calculate_black_hole_lifetime(mass)
        
        # Accretion properties
        self.accreted_mass = 0.0
        self.total_energy_radiated = 0.0
        
    def update_mass(self, delta_mass):
        """Update black hole mass (from accretion or Hawking radiation)"""
        self.mass += delta_mass
        self.accreted_mass += delta_mass if delta_mass > 0 else 0
        
        # Recalculate properties
        self.schwarzschild_radius = calculate_schwarzschild_radius(self.mass)
        self.event_horizon_radius = self.schwarzschild_radius
        self.photon_sphere_radius = 1.5 * self.schwarzschild_radius
        self.isco_radius = 3.0 * self.schwarzschild_radius
        self.temperature = calculate_hawking_temperature(self.mass)
        self.luminosity = calculate_hawking_luminosity(self.mass)
        self.lifetime = calculate_black_hole_lifetime(self.mass)
    
    def calculate_gravitational_force(self, position, mass_object):
        """
        Calculate gravitational force on an object at given position
        Returns force vector
        """
        # Vector from black hole to object
        r_vec = position - self.position
        distance = r_vec.magnitude()
        
        if distance < self.event_horizon_radius:
            # Inside event horizon - extreme force
            distance = self.event_horizon_radius
        
        # Magnitude of gravitational force
        force_magnitude = (G * self.mass * mass_object) / (distance ** 2)
        
        # Direction (towards black hole)
        force_direction = r_vec.normalize() * -1
        
        return force_direction * force_magnitude
    
    def calculate_acceleration(self, position):
        """Calculate gravitational acceleration at given position"""
        r_vec = position - self.position
        distance = r_vec.magnitude()
        
        if distance < self.event_horizon_radius:
            distance = self.event_horizon_radius
        
        # Acceleration magnitude
        accel_magnitude = (G * self.mass) / (distance ** 2)
        
        # Direction (towards black hole)
        accel_direction = r_vec.normalize() * -1
        
        return accel_direction * accel_magnitude
    
    def get_distance_from_center(self, position):
        """Get distance from black hole center"""
        return (position - self.position).magnitude()
    
    def get_distance_in_schwarzschild_radii(self, position):
        """Get distance in units of Schwarzschild radii"""
        distance = self.get_distance_from_center(position)
        return distance / self.schwarzschild_radius
    
    def is_inside_event_horizon(self, position):
        """Check if position is inside event horizon"""
        return self.get_distance_from_center(position) <= self.event_horizon_radius
    
    def is_inside_photon_sphere(self, position):
        """Check if position is inside photon sphere"""
        return self.get_distance_from_center(position) <= self.photon_sphere_radius
    
    def is_inside_isco(self, position):
        """Check if position is inside ISCO"""
        return self.get_distance_from_center(position) <= self.isco_radius
    
    def calculate_time_dilation_at(self, position):
        """Calculate time dilation factor at given position"""
        distance = self.get_distance_from_center(position)
        return calculate_time_dilation(distance, self.mass)
    
    def calculate_tidal_force_at(self, position, object_length=1.0):
        """Calculate tidal force at given position"""
        distance = self.get_distance_from_center(position)
        return calculate_tidal_force(self.mass, distance, object_length)
    
    def calculate_escape_velocity_at(self, position):
        """Calculate escape velocity at given position"""
        distance = self.get_distance_from_center(position)
        return calculate_escape_velocity(self.mass, distance)
    
    def calculate_orbital_velocity_at(self, position):
        """Calculate orbital velocity for circular orbit at given position"""
        distance = self.get_distance_from_center(position)
        return calculate_orbital_velocity(self.mass, distance)
    
    def get_zone_name(self, position):
        """Get the name of the zone where the position is located"""
        distance_rs = self.get_distance_in_schwarzschild_radii(position)
        
        if distance_rs <= EVENT_HORIZON_RADIUS:
            return "EVENT HORIZON"
        elif distance_rs <= PHOTON_SPHERE_RADIUS:
            return "PHOTON SPHERE"
        elif distance_rs <= ISCO_RADIUS:
            return "UNSTABLE ORBIT"
        elif distance_rs <= SAFE_ZONE_RADIUS:
            return "DANGER ZONE"
        else:
            return "SAFE ZONE"
    
    def get_zone_color(self, position):
        """Get color code for the zone"""
        distance_rs = self.get_distance_in_schwarzschild_radii(position)
        
        if distance_rs <= EVENT_HORIZON_RADIUS:
            return COLOR_EVENT_HORIZON
        elif distance_rs <= PHOTON_SPHERE_RADIUS:
            return COLOR_WARNING
        elif distance_rs <= ISCO_RADIUS:
            return '\033[93m'  # Yellow
        elif distance_rs <= SAFE_ZONE_RADIUS:
            return '\033[96m'  # Cyan
        else:
            return COLOR_INFO
    
    def apply_hawking_radiation(self, time_step):
        """Apply Hawking radiation mass loss"""
        # Mass loss rate (very small for stellar mass black holes)
        mass_loss_rate = -self.luminosity / (C ** 2)
        delta_mass = mass_loss_rate * time_step
        
        self.update_mass(delta_mass)
        self.total_energy_radiated += abs(delta_mass * C ** 2)
    
    def get_info_string(self):
        """Get formatted information string about the black hole"""
        info = []
        info.append(f"Mass: {format_mass(self.mass)}")
        info.append(f"Schwarzschild Radius: {format_distance(self.schwarzschild_radius)}")
        info.append(f"Event Horizon: {format_distance(self.event_horizon_radius)}")
        info.append(f"Photon Sphere: {format_distance(self.photon_sphere_radius)}")
        info.append(f"ISCO: {format_distance(self.isco_radius)}")
        info.append(f"Hawking Temp: {format_temperature(self.temperature)}")
        info.append(f"Lifetime: {format_scientific(self.lifetime)} years")
        
        if self.accreted_mass > 0:
            info.append(f"Accreted Mass: {format_scientific(self.accreted_mass)} kg")
        
        return info


class AccretionDisk:
    """Represents the accretion disk around the black hole"""
    
    def __init__(self, black_hole, num_particles=50):
        self.black_hole = black_hole
        self.particles = []
        self.num_particles = num_particles
        self.initialize_disk()
    
    def initialize_disk(self):
        """Initialize particles in the accretion disk"""
        rs = self.black_hole.schwarzschild_radius
        
        for i in range(self.num_particles):
            # Random radius between inner and outer disk
            radius_rs = np.random.uniform(DISK_INNER_RADIUS, DISK_OUTER_RADIUS)
            radius = radius_rs * rs
            
            # Random angle
            theta = np.random.uniform(0, 2 * math.pi)
            
            # Position in disk plane (z ≈ 0 with small variation)
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            z = np.random.normal(0, radius * 0.05)  # Thin disk
            
            position = Vector3D(x, y, z)
            
            # Orbital velocity
            v_orbital = calculate_orbital_velocity(self.black_hole.mass, radius)
            
            # Velocity perpendicular to radius (circular orbit)
            vx = -v_orbital * math.sin(theta)
            vy = v_orbital * math.cos(theta)
            vz = 0
            
            velocity = Vector3D(vx, vy, vz)
            
            # Temperature based on radius
            temperature = calculate_accretion_disk_temperature(radius_rs, self.black_hole.mass)
            
            self.particles.append({
                'position': position,
                'velocity': velocity,
                'temperature': temperature,
                'radius_rs': radius_rs
            })
    
    def update(self, time_step):
        """Update accretion disk particles"""
        rs = self.black_hole.schwarzschild_radius
        
        for particle in self.particles:
            # Apply gravitational acceleration
            accel = self.black_hole.calculate_acceleration(particle['position'])
            particle['velocity'] = particle['velocity'] + accel * time_step
            particle['position'] = particle['position'] + particle['velocity'] * time_step
            
            # Update radius
            distance = self.black_hole.get_distance_from_center(particle['position'])
            particle['radius_rs'] = distance / rs
            
            # Update temperature
            particle['temperature'] = calculate_accretion_disk_temperature(
                particle['radius_rs'], self.black_hole.mass
            )
            
            # Check if particle fell into black hole
            if particle['radius_rs'] < EVENT_HORIZON_RADIUS:
                # Particle is consumed - respawn at outer edge
                self.respawn_particle(particle)
    
    def respawn_particle(self, particle):
        """Respawn a particle at the outer edge of the disk"""
        rs = self.black_hole.schwarzschild_radius
        radius_rs = np.random.uniform(DISK_OUTER_RADIUS * 0.8, DISK_OUTER_RADIUS)
        radius = radius_rs * rs
        
        theta = np.random.uniform(0, 2 * math.pi)
        
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        z = np.random.normal(0, radius * 0.05)
        
        particle['position'] = Vector3D(x, y, z)
        
        v_orbital = calculate_orbital_velocity(self.black_hole.mass, radius)
        vx = -v_orbital * math.sin(theta)
        vy = v_orbital * math.cos(theta)
        vz = 0
        
        particle['velocity'] = Vector3D(vx, vy, vz)
        particle['radius_rs'] = radius_rs
        particle['temperature'] = calculate_accretion_disk_temperature(radius_rs, self.black_hole.mass)
    
    def get_particles_in_view(self):
        """Get list of disk particles for rendering"""
        return self.particles
