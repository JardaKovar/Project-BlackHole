# Black Hole Gravitational Lensing Visualization 🌌

## Overview

This is an **advanced visualization mode** that shows a realistic black hole with gravitational lensing effects, similar to the famous Event Horizon Telescope image of M87*.

## What You'll See

```
        .::::::::::::::::::.
     .:::::::::::::::::::::::.
   .:::::::::::::::::::::::::::.
  :::::::::::::::::::::::::::::::
 :::::::::::::::::::::::::::::::::
::::::::::█████████████████::::::::
:::::::::███████████████████:::::::
::::::::█████████████████████::::::
:::::::███████████████████████:::::
::::::█████████████████████████::::
:::::███████████████████████████:::
::::█████████████████████████████::
:::███████████████████████████████:
::█████████████████████████████████
:███████████████████████████████████
███████████████████████████████████
:███████████████████████████████████
::█████████████████████████████████
:::███████████████████████████████:
::::█████████████████████████████::
:::::███████████████████████████:::
::::::█████████████████████████::::
:::::::███████████████████████:::::
::::::::█████████████████████::::::
:::::::::███████████████████:::::::
::::::::::█████████████████::::::::
 :::::::::::::::::::::::::::::::::
  :::::::::::::::::::::::::::::::
   .:::::::::::::::::::::::::::.
     .:::::::::::::::::::::::.
        .::::::::::::::::::.
```

## Features

### Gravitational Lensing Effects
- **Event Horizon** (black center) - The point of no return
- **Photon Ring** (bright yellow ring) - Light orbiting at 1.5 Rs
- **Accretion Disk** (orange/red) - Hot matter spiraling inward
- **Doppler Boosting** - One side appears brighter due to relativistic motion
- **Light Bending** - Realistic gravitational lensing calculations

### Color Coding
- **Black** - Event horizon (no light escapes)
- **Dark Red** - Outer glow and scattered light
- **Red** - Cool outer accretion disk (~10,000 K)
- **Orange** - Mid-temperature disk (~100,000 K)
- **Yellow-Orange** - Hot inner disk (~1,000,000 K)
- **Yellow** - Very hot inner disk (~10,000,000 K)
- **Bright Yellow** - Photon ring (light trapped in orbit)

### Physics Simulation
- Temperature gradient in accretion disk
- Doppler shift from rotating disk
- Gravitational redshift
- Light bending calculations
- Particle dynamics with black hole gravity

## How to Run

### Quick Start
```bash
python black_hole_lensing.py
```

### Controls
- **SPACE** - Add a particle to the simulation
- **C** - Clear all particles
- **Q** - Quit the visualization

## Technical Details

### Rendering Method
The visualization uses:
1. **Ray tracing** through curved spacetime
2. **Schwarzschild metric** for gravitational field
3. **Temperature-based coloring** for accretion disk
4. **ASCII/Unicode characters** for brightness levels
5. **ANSI color codes** for temperature representation

### Brightness Characters
From dark to bright: ` .:-=+*#%@`

### Physics Parameters
- **Black Hole Mass**: 10 solar masses (default)
- **Schwarzschild Radius**: ~29.5 km
- **Photon Sphere**: 1.5 Rs (~44.3 km)
- **ISCO**: 3 Rs (~88.6 km)
- **Disk Temperature**: 10⁷ K (inner) to 10⁴ K (outer)

## Comparison with Real Black Holes

This visualization is inspired by:
- **M87*** - First black hole image (2019)
- **Sagittarius A*** - Milky Way's black hole (2022)
- **Interstellar** movie visualization (2014)

### Similarities
✅ Photon ring structure
✅ Asymmetric brightness (Doppler boosting)
✅ Accretion disk appearance
✅ Event horizon shadow
✅ Temperature gradient colors

### Simplifications
⚠️ 2D projection (real black holes are 3D)
⚠️ Schwarzschild (non-rotating) vs Kerr (rotating)
⚠️ Simplified ray tracing
⚠️ ASCII art vs high-resolution imaging

## Files

- `black_hole_lensing.py` - Main program
- `lensing_renderer.py` - Gravitational lensing renderer
- `black_hole_physics.py` - Physics engine
- `particle_system.py` - Particle dynamics
- `config.py` - Configuration
- `utils.py` - Utilities

## Switching Between Modes

### Lensing Visualization (Realistic)
```bash
python black_hole_lensing.py
```
Shows the black hole as it would appear with gravitational lensing.

### Interactive Simulation (Original)
```bash
python black_hole_sim.py
```
Shows particles, orbits, and interactive controls.

## Educational Value

This visualization demonstrates:
- **General Relativity** - Curved spacetime
- **Gravitational Lensing** - Light bending
- **Black Hole Thermodynamics** - Temperature gradients
- **Relativistic Effects** - Doppler boosting
- **Accretion Physics** - Matter spiraling inward

## Performance

- **Resolution**: 120×40 characters
- **Frame Rate**: ~30 FPS
- **Calculation**: Real-time lensing computation
- **Memory**: ~50 MB

## Customization

Edit `lensing_renderer.py` to adjust:
- Color palette
- Brightness levels
- Disk thickness
- Temperature distribution
- Lensing strength

## References

1. Event Horizon Telescope Collaboration (2019) - M87* Image
2. Schwarzschild, K. (1916) - Schwarzschild Metric
3. Luminet, J.-P. (1979) - Black Hole Visualization
4. James, O. et al. (2015) - Interstellar Black Hole

## Credits

Based on:
- Einstein's General Relativity
- Schwarzschild solution
- Accretion disk physics
- Computational astrophysics

---

**Enjoy exploring the universe! 🌌✨**
