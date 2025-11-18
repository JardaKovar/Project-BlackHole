# Project-BlackHole 🌌

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An interactive 3D black hole simulation built with Python and Pygame, featuring realistic physics, beautiful visuals, and full 3D camera controls.

![Black Hole Simulation](https://via.placeholder.com/800x400/000000/FFFFFF?text=Black+Hole+Ultimate+Simulation)

## ✨ Features

- **Full 3D Rotation**: Explore the black hole from any angle with mouse controls
- **Realistic Physics**: Newtonian gravity with particle dynamics
- **Beautiful Accretion Disk**: Temperature-based color gradients from white-hot to deep red
- **Particle System**: Interactive particles with orbital mechanics and trails
- **Smooth Performance**: 60 FPS rendering with optimized graphics
- **Interactive Controls**: Add particles, pause, zoom, and reset simulation

## 🎮 Demo

Experience gravitational physics in action:
- Watch particles orbit and spiral into the black hole
- Rotate the camera to see the 3D structure
- Observe color-coded accretion disk temperatures
- Add new particles with right-click

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JardaKovar/Project-BlackHole.git
   cd Project-BlackHole
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the simulation**:
   ```bash
   python black_hole_ultimate.py
   ```

## 🎯 Controls

| Control | Action |
|---------|--------|
| **Mouse Drag** | Rotate 3D view |
| **Mouse Wheel** | Zoom in/out |
| **Right Click** | Add particle |
| **SPACE** | Pause/Resume |
| **R** | Reset particles |
| **ESC** | Quit |

## 📁 Project Structure

```
Project-BlackHole/
├── black_hole_ultimate.py    # Main simulation
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── QUICKSTART.md            # Quick start guide
├── TUTORIAL.md              # Detailed tutorial
└── README.md                # This file
```

## 🔬 Physics

The simulation implements:
- **Gravitational Force**: `F = GMm/r²`
- **Particle Dynamics**: Position and velocity integration
- **Event Horizon**: Capture radius at 5 units
- **Accretion Disk**: Temperature gradient visualization
- **Orbital Mechanics**: Stable and unstable orbits

## 🎨 Visual Features

- **3D Perspective Projection**: Depth-sorted rendering
- **Soft Gradients**: Smooth color transitions
- **Glow Effects**: Atmospheric rings around the black hole
- **Particle Trails**: Cyan trails showing orbital paths
- **Dynamic Colors**: Speed and temperature-based coloring

## 📖 Documentation

- **[TUTORIAL.md](TUTORIAL.md)**: Comprehensive guide with physics explanations
- **[QUICKSTART.md](QUICKSTART.md)**: Quick setup and basic usage

## 🛠️ Customization

Modify `config.py` to adjust:
- Black hole properties
- Simulation parameters
- Visual settings
- Performance options

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Physics based on General Relativity principles
- Built with Pygame for smooth graphics
- Inspired by real astronomical simulations

## 🌟 Star this repo if you find it interesting!

---

**Explore the fascinating world of black holes!** 🚀✨

[View on GitHub](https://github.com/JardaKovar/Project-BlackHole) | [Tutorial](TUTORIAL.md) | [Quick Start](QUICKSTART.md)






# Tutorial: Black Hole Ultimate Simulation 🌌

Welcome to the **Black Hole Ultimate** simulation! This interactive 3D visualization combines beautiful soft gradients, full 3D rotation, and realistic particle physics to bring black holes to life on your screen.

## 🎯 What This Simulation Does

This program creates a stunning 3D visualization of a black hole with:
- **Realistic accretion disk** with temperature-based color gradients
- **Full 3D camera controls** for exploring the black hole from any angle
- **Particle physics simulation** with gravitational effects
- **Smooth animations** at 60 FPS
- **Interactive controls** for a hands-on experience

## 📋 Requirements

- **Python 3.7+**
- **Pygame library**
- **NumPy library**
- A graphics-capable computer (for smooth 60 FPS performance)

## 🚀 Installation

1. **Ensure Python is installed** (version 3.7 or higher)

2. **Install required libraries**:
   ```bash
   pip install pygame numpy
   ```

3. **Download the code**: `black_hole_ultimate.py` from this repository

## 🎮 Running the Simulation

### Basic Launch
```bash
python black_hole_ultimate.py
```

### What You'll See
When you run the program, you'll see:
- A black sphere representing the black hole
- A colorful, rotating accretion disk around it
- Glowing rings showing gravitational effects
- Moving particles (green dots) with cyan trails
- Real-time FPS and particle count display

## 🎮 Controls Guide

### Camera Controls
| Control | Action | Description |
|---------|--------|-------------|
| **Left Mouse + Drag** | Rotate view | Full 3D rotation around the black hole |
| **Mouse Wheel** | Zoom | Zoom in/out (distance: 80-250 units) |

### Particle Controls
| Control | Action | Description |
|---------|--------|-------------|
| **Right Click** | Add particle | Spawn a new particle with random orbital velocity |
| **R Key** | Reset particles | Clear all particles and add 8 new ones |
| **SPACE** | Pause/Resume | Freeze or unfreeze the simulation |

### Program Controls
| Control | Action | Description |
|---------|--------|-------------|
| **ESC** | Quit | Exit the simulation |
| **SPACE** | Pause | Toggle simulation pause |

## 🌟 Features Explained

### 1. The Black Hole
- **Black Sphere**: The event horizon (point of no return)
- **Size**: Fixed radius of 5 units
- **Physics**: Particles within 5 units are captured

### 2. Accretion Disk
- **Structure**: Thousands of particles arranged in concentric rings
- **Colors**: Temperature-based gradients from white-hot (inner) to deep red (outer)
- **Rotation**: Slowly rotates to simulate orbital motion
- **Soft Gradients**: Smooth color transitions for realistic appearance

### 3. Glow Rings
- **Purpose**: Visual representation of gravitational influence
- **Colors**: Orange-to-red gradient fading with distance
- **Physics**: Represent regions of strong tidal forces

### 4. Particles
- **Behavior**: Orbit under gravitational influence
- **Colors**: Green (slow), Orange (medium), Red (fast)
- **Trails**: Cyan lines showing recent paths
- **Lifespan**: Automatically removed when captured or escaped

### 5. 3D Camera System
- **Rotation**: Full X and Y axis rotation
- **Projection**: Perspective projection with depth sorting
- **Zoom**: Dynamic distance adjustment
- **Limits**: Prevents upside-down viewing

## 🔬 Physics Behind the Simulation

### Gravitational Physics
- **Force**: `F = GMm/r²` (Newtonian gravity)
- **Strength**: G = 100.0 (scaled for simulation)
- **Direction**: Always towards the black hole center

### Particle Motion
- **Integration**: Simple Euler method for position/velocity updates
- **Timestep**: Variable based on frame rate
- **Boundaries**: Captured at r < 5, escaped at r > 200

### Color Coding
- **Temperature Gradient**: Based on distance from black hole
- **Inner Disk**: White → Yellow → Orange → Red
- **Particle Speed**: Green (slow) → Orange → Red (fast)

### Visual Effects
- **Depth Sorting**: Farther objects drawn first
- **Size Scaling**: Objects appear smaller with distance
- **Trail Rendering**: Recent positions connected with lines

## 🎨 Customization

### Modifying the Code

#### Change Black Hole Size
```python
# In the BlackHoleUltimate class
# Change the radius in generate_disk_particles and draw_black_hole_sphere
radius = 5  # Change this value
```

#### Adjust Gravitational Strength
```python
# In Particle.update()
accel = -100.0 * self.pos / (r ** 2)  # Change 100.0
```

#### Modify Colors
```python
# In generate_disk_particles()
# Adjust the color calculation logic
if temp > 0.8:
    color = (255, 255, int(220 + 35 * (temp - 0.8) / 0.2))
# Change RGB values as desired
```

#### Change Particle Count
```python
# In add_random_particles()
for _ in range(count):  # Change count parameter
```

## 🧪 Experiments to Try

### 1. Orbital Mechanics
- Add particles at different distances
- Observe stable vs. unstable orbits
- Watch particles spiral inward

### 2. Escape Velocity
- Right-click to add particles
- See which ones escape vs. get captured
- Try adding particles with different initial velocities

### 3. Camera Exploration
- Rotate around to see different perspectives
- Zoom in close to the accretion disk
- Observe how the view changes with distance

### 4. Performance Testing
- Add many particles (right-click repeatedly)
- See how FPS changes
- Test on different hardware

### 5. Visual Analysis
- Pause the simulation (SPACE)
- Study the accretion disk structure
- Count the number of visible rings

## 🔧 Troubleshooting

### Common Issues

#### "pygame not found" Error
```bash
pip install pygame
```

#### Low FPS (< 30)
- Close other programs
- Reduce screen resolution in code
- Lower particle count

#### Particles Not Moving
- Check if simulation is paused (look for "PAUSED" text)
- Press SPACE to resume

#### Black Screen
- Ensure graphics drivers are up to date
- Try running in a different terminal/command prompt

#### Controls Not Working
- Make sure the window has focus (click on it)
- Try pressing keys multiple times

### Performance Tips
- **Reduce Disk Particles**: Lower the range in `generate_disk_particles()`
- **Fewer Segments**: Decrease `segments` variable
- **Disable Trails**: Comment out trail drawing code
- **Lower FPS**: Change `FPS = 60` to lower value

## 📚 Code Structure

### Main Classes

#### `Camera`
- Handles 3D rotation and projection
- Methods: `rotate()`, `zoom()`, `project()`

#### `Particle`
- Represents individual particles
- Physics: position, velocity, trail
- Methods: `update()`

#### `BlackHoleUltimate`
- Main simulation class
- Contains all rendering and update logic
- Methods: `draw_*()`, `handle_events()`, `update()`

### Key Functions
- `generate_disk_particles()`: Creates the accretion disk
- `draw_accretion_disk_3d()`: Renders the disk in 3D
- `draw_black_hole_sphere()`: Draws the black hole
- `draw_soft_glow_rings()`: Adds atmospheric effects

## 🎓 Learning Outcomes

After exploring this simulation, you'll understand:
- **3D Graphics**: Perspective projection and depth sorting
- **Physics Simulation**: Gravitational force calculations
- **Particle Systems**: Managing many moving objects
- **Interactive Controls**: Mouse and keyboard input handling
- **Real-time Rendering**: Balancing performance and visuals

## 🚀 Advanced Modifications

### Add New Features
- **Sound Effects**: Add audio for particle capture
- **Multiple Black Holes**: Simulate binary systems
- **Magnetic Fields**: Add particle deflection
- **Time Controls**: Variable speed simulation

### Physics Enhancements
- **Relativistic Effects**: Proper time dilation
- **General Relativity**: More accurate gravity near the event horizon
- **Radiation Pressure**: Particles pushed by light

### Visual Improvements
- **Shaders**: GLSL effects for better gradients
- **Textures**: Add surface detail to the black hole
- **Post-processing**: Bloom and motion blur effects

## 📞 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your Python and library versions
3. Try running with minimal settings
4. Check the console output for error messages

## 🌟 Next Steps

- Explore the other simulation files in this repository
- Try modifying the code to add new features
- Learn more about black hole physics
- Share your modifications with the community!

---

**Enjoy exploring the mysteries of black holes!** 🚀✨

*This tutorial was created for the Black Hole Ultimate simulation. For more information, see the main README.md file.*
