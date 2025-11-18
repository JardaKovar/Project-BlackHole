# Black Hole Simulation 🌌

A super detailed, physics-accurate black hole simulation that runs in your terminal (CMD/bash). Experience the fascinating physics of black holes with real-time particle interactions, accretion disks, and relativistic effects!

![Black Hole Simulation](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Physics](https://img.shields.io/badge/Physics-Accurate-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## 🌟 Features

### Physics Simulation
- **Realistic Gravitational Physics**: Accurate Newtonian gravity calculations
- **Schwarzschild Black Hole**: Based on Einstein's General Relativity
- **Event Horizon**: The point of no return (1 Rs)
- **Photon Sphere**: Where light orbits the black hole (1.5 Rs)
- **ISCO**: Innermost Stable Circular Orbit (3 Rs)
- **Time Dilation**: Gravitational time dilation effects
- **Hawking Radiation**: Black hole evaporation (theoretical)
- **Spaghettification**: Tidal forces that stretch objects
- **Accretion Disk**: Rotating disk of matter with temperature gradients

### Visualization
- **Multiple View Modes**: Top-down, side view, and 3D projection
- **Color-Coded Zones**: Visual distinction between safe and dangerous regions
- **Particle Trails**: See the paths particles take
- **Real-Time Statistics**: Monitor black hole properties and particle counts
- **Smooth Animation**: 30 FPS terminal rendering
- **Zoom Controls**: Adjust view scale dynamically

### Interactive Controls
- Add particles on demand
- Pause/resume simulation
- Change view perspectives
- Adjust simulation speed
- Toggle visual elements
- Reset simulation

## 📋 Requirements

- Python 3.7 or higher
- Terminal with ANSI color support
- Windows (CMD/PowerShell) or Unix-like system (bash, zsh, etc.)

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install numpy colorama
   ```

## 🎮 Usage

### Running the Simulation

**Windows (CMD/PowerShell)**:
```cmd
python black_hole_sim.py
```

**Linux/macOS (bash/zsh)**:
```bash
python3 black_hole_sim.py
```

### Controls

| Key | Action |
|-----|--------|
| `SPACE` | Add a new particle |
| `P` | Pause/Resume simulation |
| `V` | Change view mode (Top/Side/3D) |
| `+` / `-` | Zoom in/out |
| `[` / `]` | Slow down/Speed up simulation |
| `G` | Toggle coordinate grid |
| `T` | Toggle particle trails |
| `A` | Toggle accretion disk |
| `S` | Toggle auto-spawn particles |
| `C` | Clear all particles |
| `R` | Reset simulation |
| `Q` | Quit |

## 🔬 Physics Explained

### Black Hole Properties

**Schwarzschild Radius (Rs)**:
```
Rs = 2GM/c²
```
Where:
- G = Gravitational constant (6.674×10⁻¹¹ m³ kg⁻¹ s⁻²)
- M = Black hole mass
- c = Speed of light (299,792,458 m/s)

**Default Black Hole**: 10 solar masses (1.989×10³¹ kg)
- Schwarzschild Radius: ~29.5 km
- Event Horizon: 29.5 km
- Photon Sphere: 44.3 km
- ISCO: 88.6 km

### Zones

1. **Event Horizon (1 Rs)** - Red
   - Point of no return
   - Escape velocity = speed of light
   - Time appears to stop from outside observer

2. **Photon Sphere (1.5 Rs)** - Yellow
   - Unstable orbit for photons
   - Light can orbit the black hole

3. **ISCO (3 Rs)** - Orange
   - Innermost Stable Circular Orbit
   - Closest stable orbit for matter

4. **Danger Zone (3-10 Rs)** - Cyan
   - Strong gravitational effects
   - High tidal forces

5. **Safe Zone (>10 Rs)** - White
   - Relatively safe region
   - Normal orbital mechanics apply

### Time Dilation

Time dilation factor at distance r:
```
t' = t × √(1 - Rs/r)
```

At the event horizon, time dilation becomes infinite (time stops).

### Hawking Radiation

Black holes emit thermal radiation with temperature:
```
T = ℏc³/(8πGMk_B)
```

For a 10 solar mass black hole:
- Temperature: ~6.2×10⁻⁹ K
- Evaporation time: ~2×10⁶⁷ years

### Accretion Disk

The accretion disk is a rotating disk of matter spiraling into the black hole:
- **Inner Edge**: ISCO (3 Rs)
- **Outer Edge**: ~20 Rs
- **Temperature**: Decreases with radius (10⁷ K inner → 10⁴ K outer)
- **Emission**: X-rays and gamma rays from inner regions

### Tidal Forces (Spaghettification)

The difference in gravitational force across an object:
```
ΔF = 2GMl/r³
```

Where l is the object's length. This stretches objects radially and compresses them tangentially.

## 📊 Statistics Display

The simulation displays real-time information:

### Black Hole Info
- Mass (in solar masses)
- Schwarzschild radius
- Hawking temperature
- Estimated lifetime

### Particle Statistics
- Active particles
- Total created
- Captured by black hole
- Escaped to infinity

### Simulation Info
- Elapsed time
- Current FPS
- View mode
- Zoom level

## 🎨 Visualization

### Color Coding

- **Magenta (●)**: Black hole center
- **Red (█)**: Event horizon
- **Yellow (○)**: Photon sphere
- **Orange (·)**: ISCO
- **Cyan (~)**: Accretion disk
- **Green/Red (•)**: Particles (color varies with temperature/speed)
- **Faded (·)**: Particle trails

### View Modes

1. **Top View**: X-Y plane (looking down)
2. **Side View**: X-Z plane (looking from the side)
3. **3D View**: Perspective projection with rotation

## 🧪 Experiments to Try

1. **Orbital Mechanics**
   - Add particles at different distances
   - Observe stable vs unstable orbits
   - Watch particles spiral into the black hole

2. **Escape Velocity**
   - Add fast-moving particles
   - See which ones escape vs get captured

3. **Accretion Disk**
   - Watch the disk particles spiral inward
   - Observe temperature changes

4. **Spaghettification**
   - Watch particles get stretched near the event horizon
   - Observe tidal effects

5. **Time Dilation**
   - Compare particle speeds at different distances
   - Notice relativistic effects near the black hole

## 🔧 Configuration

Edit `config.py` to customize:

- Black hole mass
- Simulation speed
- Display settings
- Particle parameters
- Physics constants
- Color schemes

Example:
```python
# Change black hole mass to 100 solar masses
BLACK_HOLE_MASS = 100 * SOLAR_MASS

# Increase particle spawn rate
PARTICLE_SPAWN_RATE = 0.3

# Change screen size
SCREEN_WIDTH = 150
SCREEN_HEIGHT = 50
```

## 📁 Project Structure

```
PythonBlackhole/
├── black_hole_sim.py      # Main simulation program
├── black_hole_physics.py  # Black hole physics calculations
├── particle_system.py     # Particle management
├── visualization.py       # Terminal rendering
├── utils.py              # Utility functions
├── config.py             # Configuration and constants
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🐛 Troubleshooting

### Colors not displaying
- Ensure your terminal supports ANSI colors
- On Windows, use Windows Terminal or enable ANSI in CMD
- The `colorama` package should handle this automatically

### Slow performance
- Reduce `MAX_PARTICLES` in config.py
- Decrease `FRAME_RATE`
- Disable particle trails (press `T`)
- Disable accretion disk (press `A`)

### Input not working
- On Windows, the simulation uses `msvcrt` for input
- On Unix, input handling is simplified
- Try pressing keys multiple times

### Screen flickering
- This is normal for terminal-based animations
- Use a terminal with better refresh rates
- Reduce frame rate if needed

## 🎓 Educational Value

This simulation demonstrates:
- **General Relativity**: Schwarzschild solution
- **Classical Mechanics**: Orbital dynamics
- **Thermodynamics**: Hawking radiation
- **Computational Physics**: Numerical integration
- **Computer Graphics**: 3D projection and rendering

Perfect for:
- Physics students
- Astronomy enthusiasts
- Science educators
- Anyone curious about black holes!

## 📚 References

- Einstein, A. (1915). "General Theory of Relativity"
- Schwarzschild, K. (1916). "On the Gravitational Field of a Mass Point"
- Hawking, S. (1974). "Black hole explosions?"
- Misner, Thorne, Wheeler (1973). "Gravitation"

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Improve physics accuracy
- Enhance visualization
- Add new view modes

## 📄 License

This project is open source and available for educational purposes.

## 🌟 Acknowledgments

- Physics equations based on General Relativity
- Inspired by real black hole simulations
- Built with Python and love for physics!

## 🚀 Future Enhancements

Potential additions:
- Rotating (Kerr) black holes
- Gravitational lensing effects
- Binary black hole systems
- Gravitational waves
- More realistic accretion disk physics
- Save/load simulation states
- Export data for analysis

---

**Enjoy exploring the fascinating physics of black holes!** 🌌✨

For questions or feedback, feel free to reach out!
