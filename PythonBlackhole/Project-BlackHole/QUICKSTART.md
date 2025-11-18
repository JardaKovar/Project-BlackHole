# Quick Start Guide 🚀

Get your black hole simulation running in 3 easy steps!

## Step 1: Install Dependencies

```bash
pip install numpy colorama
```

## Step 2: Run the Simulation

**Windows:**
```cmd
python black_hole_sim.py
```

**Linux/macOS:**
```bash
python3 black_hole_sim.py
```

## Step 3: Interact!

Press **SPACE** to add particles and watch them orbit or fall into the black hole!

### Essential Controls

- **SPACE** - Add particle
- **V** - Change view
- **Q** - Quit

### What You'll See

```
╔═══ BLACK HOLE SIMULATION ═══╗
Black Hole:
  Mass: 10.00 M☉
  Rs: 29.54 km
  
Particles:
  Active: 5/100
  Captured: 2
  
Controls:
  SPACE: Add particle
  V: Change view
  Q: Quit
```

The simulation shows:
- **●** (Magenta) - Black hole center
- **█** (Red) - Event horizon (point of no return)
- **○** (Yellow) - Photon sphere
- **~** (Cyan) - Accretion disk
- **•** (Green/Red) - Particles

### Tips

1. **Add multiple particles** - Press SPACE several times
2. **Change perspective** - Press V to cycle views
3. **Zoom in/out** - Use +/- keys
4. **Watch the physics** - Particles orbit, spiral, or escape!

### What's Happening?

- Particles are affected by the black hole's gravity
- Some orbit stably, others spiral inward
- Particles crossing the event horizon are captured
- The accretion disk shows matter spiraling into the black hole
- Colors indicate temperature and danger zones

## Troubleshooting

**No colors?**
- Make sure colorama is installed: `pip install colorama`

**Simulation won't start?**
- Check Python version: `python --version` (need 3.7+)
- Install numpy: `pip install numpy`

**Controls not working?**
- Try pressing keys multiple times
- On Windows, use CMD or PowerShell

## Next Steps

- Read the full [README.md](README.md) for detailed physics explanations
- Experiment with different controls
- Try changing settings in `config.py`
- Learn about black hole physics!

---

**Have fun exploring the universe! 🌌**
