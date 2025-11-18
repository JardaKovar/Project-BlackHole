"""
Particle System Module
Handles individual particles and their interactions with the black hole
"""

import math
import random
import numpy as np
from config import *
from utils import *
from black_hole_physics import BlackHole


class Particle:
    """Represents a particle affected by the black hole's gravity"""
    
    def __init__(self, position, velocity, mass=1000.0, particle_id=0):
        self.id = particle_id
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.mass = mass
        self.acceleration = Vector3D(0, 0, 0)
        
        # Trail for visualization
        self.trail = []
        self.max_trail_length = TRAIL_LENGTH
        
        # State tracking
        self.is_alive = True
        self.is_captured = False
        self.time_alive = 0.0
        self.distance_traveled = 0.0
        
        # Physics properties
        self.kinetic_energy = 0.0
        self.potential_energy = 0.0
        self.total_energy = 0.0
        self.angular_momentum = Vector3D(0, 0, 0)
        
        # Visual properties
        self.color = COLOR_PARTICLE
        self.char = CHAR_PARTICLE
        self.temperature = 300.0  # Kelvin
        
    def update(self, black_hole, time_step):
        """Update particle position and velocity"""
        if not self.is_alive:
            return
        
        # Store previous position for trail
        prev_position = self.position.copy()
        
        # Calculate gravitational acceleration
        self.acceleration = black_hole.calculate_acceleration(self.position)
        
        # Update velocity (Verlet integration for better accuracy)
        self.velocity = self.velocity + self.acceleration * time_step
        
        # Check for relativistic effects
        speed = self.velocity.magnitude()
        if speed > C * 0.1:  # If speed > 10% of light speed
            # Apply relativistic correction
            gamma = calculate_relativistic_factor(speed)
            if gamma < 100:  # Avoid extreme values
                self.velocity = self.velocity / gamma
        
        # Update position
        self.position = self.position + self.velocity * time_step
        
        # Update trail
        self.trail.append(prev_position)
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Update distance traveled
        displacement = (self.position - prev_position).magnitude()
        self.distance_traveled += displacement
        
        # Update time alive
        self.time_alive += time_step
        
        # Calculate energies
        self.update_energies(black_hole)
        
        # Calculate angular momentum
        r_vec = self.position - black_hole.position
        self.angular_momentum = r_vec.cross(self.velocity) * self.mass
        
        # Check if particle crossed event horizon
        if black_hole.is_inside_event_horizon(self.position):
            self.is_captured = True
            self.is_alive = False
            self.color = COLOR_EVENT_HORIZON
            return
        
        # Update visual properties based on physics
        self.update_visual_properties(black_hole)
    
    def update_energies(self, black_hole):
        """Calculate kinetic and potential energies"""
        # Kinetic energy (classical approximation)
        speed = self.velocity.magnitude()
        self.kinetic_energy = 0.5 * self.mass * speed ** 2
        
        # Gravitational potential energy
        distance = black_hole.get_distance_from_center(self.position)
        if distance > 0:
            self.potential_energy = -(G * black_hole.mass * self.mass) / distance
        else:
            self.potential_energy = 0
        
        # Total mechanical energy
        self.total_energy = self.kinetic_energy + self.potential_energy
    
    def update_visual_properties(self, black_hole):
        """Update color and character based on particle state"""
        distance_rs = black_hole.get_distance_in_schwarzschild_radii(self.position)
        speed = self.velocity.magnitude()
        
        # Calculate temperature based on kinetic energy (simplified)
        self.temperature = (self.kinetic_energy / (1.5 * K_B)) if self.kinetic_energy > 0 else 300
        
        # Color based on zone and speed
        if distance_rs <= PHOTON_SPHERE_RADIUS:
            self.color = COLOR_EVENT_HORIZON
            self.char = '◆'
        elif distance_rs <= ISCO_RADIUS:
            self.color = COLOR_WARNING
            self.char = '◇'
        elif speed > C * 0.01:  # Fast moving
            self.color = get_color_from_temperature(self.temperature)
            self.char = '●'
        else:
            self.color = COLOR_PARTICLE
            self.char = CHAR_PARTICLE
    
    def apply_spaghettification(self, black_hole):
        """Apply tidal forces (spaghettification effect)"""
        # Assume particle has some length (1 meter)
        tidal_force = black_hole.calculate_tidal_force_at(self.position, 1.0)
        
        # If tidal force is extreme, particle is destroyed
        if tidal_force > 1e10:  # Arbitrary threshold
            self.is_alive = False
            self.is_captured = True
    
    def get_info_string(self):
        """Get formatted information about the particle"""
        info = []
        info.append(f"Particle #{self.id}")
        info.append(f"Position: ({self.position.x:.2e}, {self.position.y:.2e}, {self.position.z:.2e}) m")
        info.append(f"Velocity: {self.velocity.magnitude():.2e} m/s ({self.velocity.magnitude()/C*100:.4f}% c)")
        info.append(f"Speed: {format_scientific(self.velocity.magnitude())} m/s")
        info.append(f"KE: {format_scientific(self.kinetic_energy)} J")
        info.append(f"PE: {format_scientific(self.potential_energy)} J")
        info.append(f"Total E: {format_scientific(self.total_energy)} J")
        info.append(f"Distance: {format_distance(self.position.magnitude())}")
        info.append(f"Time Alive: {self.time_alive:.2f} s")
        info.append(f"Distance Traveled: {format_distance(self.distance_traveled)}")
        
        return info


class ParticleSystem:
    """Manages multiple particles in the simulation"""
    
    def __init__(self, black_hole):
        self.black_hole = black_hole
        self.particles = []
        self.next_particle_id = 0
        self.total_particles_created = 0
        self.total_particles_captured = 0
        self.total_particles_escaped = 0
    
    def add_particle(self, position=None, velocity=None, mass=1000.0):
        """Add a new particle to the system"""
        if len(self.particles) >= MAX_PARTICLES:
            return None
        
        # Generate random position if not provided
        if position is None:
            position = self.generate_random_position()
        
        # Generate random velocity if not provided
        if velocity is None:
            velocity = self.generate_random_velocity(position)
        
        particle = Particle(position, velocity, mass, self.next_particle_id)
        self.particles.append(particle)
        self.next_particle_id += 1
        self.total_particles_created += 1
        
        return particle
    
    def generate_random_position(self):
        """Generate a random position for a new particle"""
        rs = self.black_hole.schwarzschild_radius
        
        # Random distance from black hole
        distance_rs = random.uniform(PARTICLE_INITIAL_DISTANCE_MIN, PARTICLE_INITIAL_DISTANCE_MAX)
        distance = distance_rs * rs
        
        # Random direction (spherical coordinates)
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        
        x = distance * math.sin(phi) * math.cos(theta)
        y = distance * math.sin(phi) * math.sin(theta)
        z = distance * math.cos(phi)
        
        return Vector3D(x, y, z)
    
    def generate_random_velocity(self, position):
        """Generate a random velocity for a particle at given position"""
        # Calculate orbital velocity at this distance
        distance = position.magnitude()
        v_orbital = calculate_orbital_velocity(self.black_hole.mass, distance)
        
        # Add some randomness (0.5 to 1.5 times orbital velocity)
        v_magnitude = v_orbital * random.uniform(0.5, 1.5)
        
        # Random direction (mostly tangential for interesting orbits)
        # Get perpendicular direction to radius
        radius_normalized = position.normalize()
        
        # Create a perpendicular vector
        if abs(radius_normalized.z) < 0.9:
            perpendicular = Vector3D(0, 0, 1).cross(radius_normalized)
        else:
            perpendicular = Vector3D(1, 0, 0).cross(radius_normalized)
        
        perpendicular = perpendicular.normalize()
        
        # Rotate around radius to get random tangential direction
        angle = random.uniform(0, 2 * math.pi)
        
        # Mix radial and tangential components
        radial_component = radius_normalized * random.uniform(-0.3, 0.3)
        tangential_component = perpendicular * random.uniform(0.7, 1.0)
        
        velocity_direction = (radial_component + tangential_component).normalize()
        
        return velocity_direction * v_magnitude
    
    def update(self, time_step):
        """Update all particles"""
        particles_to_remove = []
        
        for particle in self.particles:
            if particle.is_alive:
                particle.update(self.black_hole, time_step)
                
                # Check if particle escaped (too far away)
                distance_rs = self.black_hole.get_distance_in_schwarzschild_radii(particle.position)
                if distance_rs > 100:  # Escaped
                    particle.is_alive = False
                    self.total_particles_escaped += 1
                    particles_to_remove.append(particle)
                
                # Check if particle was captured
                if particle.is_captured:
                    self.total_particles_captured += 1
                    # Add mass to black hole
                    self.black_hole.update_mass(particle.mass)
                    particles_to_remove.append(particle)
            else:
                particles_to_remove.append(particle)
        
        # Remove dead particles
        for particle in particles_to_remove:
            if particle in self.particles:
                self.particles.remove(particle)
    
    def spawn_random_particle(self):
        """Spawn a particle with random properties"""
        if random.random() < PARTICLE_SPAWN_RATE:
            self.add_particle()
    
    def get_active_particles(self):
        """Get list of active particles"""
        return [p for p in self.particles if p.is_alive]
    
    def get_statistics(self):
        """Get statistics about the particle system"""
        stats = {
            'active': len(self.get_active_particles()),
            'total_created': self.total_particles_created,
            'captured': self.total_particles_captured,
            'escaped': self.total_particles_escaped,
        }
        return stats
    
    def clear_all(self):
        """Remove all particles"""
        self.particles.clear()
    
    def add_particle_at_cursor(self, x, y, z=0):
        """Add a particle at specific coordinates"""
        position = Vector3D(x, y, z)
        velocity = self.generate_random_velocity(position)
        return self.add_particle(position, velocity)
