# Changelog

All notable changes to the N-Body Solar System Simulator are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [v1.0.0] — 2026-06-12

### 🚀 Initial Production Release

First stable release of the Interactive N-Body Solar System Simulator.

### Added

- **Dash UI** — Full-screen interactive 3D orbital visualization using Plotly Scatter3d
- **SciPy ODE Integration** — RK45 adaptive Runge-Kutta solver via `scipy.integrate.solve_ivp`
  - Configurable `rtol=1e-8`, `atol=1e-10` for high-accuracy integration
  - Softening length to prevent singularity at close approach
- **NASA JPL Horizons Ephemeris Client**
  - Live REST API queries for Cartesian state vectors (J2000.0 ecliptic frame)
  - Solar System Barycenter (`@0`) as reference center
  - AU/day unit system for direct ODE compatibility
- **Real-Time Orbital Mechanics**
  - Full 9-body system: Sun + 8 planets
  - Configurable simulation duration: 30 days to 10 years
  - Body selection checklist for custom configurations
- **Visual Design**
  - Deep space dark theme (CSS)
  - Per-body color coding and size scaling
  - Current-position markers with body labels
- **Modular Architecture**
  - `simulator/bodies.py` — body data models and physical constants
  - `simulator/ephemeris.py` — JPL Horizons API client
  - `simulator/nbody.py` — gravitational ODE solver
  - `app.py` — Dash application and callback layer

### Physics Model

```
d²rᵢ/dt² = G × Σⱼ≠ᵢ mⱼ(rⱼ − rᵢ) / |rⱼ − rᵢ|³
```

Integrated via SciPy RK45 with `max_step=3600s` (1 hour) for solar system dynamics.

### Known Limitations (v1.0.0)

- Relativistic corrections (GR) not yet implemented
- No Moon or dwarf planet data by default (configurable)
- Trajectory animation (frame-by-frame) planned for v1.1.0

---

## Upcoming

### [v1.1.0] — Planned
- Real-time animation with frame slider
- Energy conservation diagnostics panel
- Export trajectories to CSV/Parquet
- Additional bodies: Moon, Pluto, Ceres

### [v1.2.0] — Planned
- Post-Newtonian (1PN) relativistic corrections
- WebSocket streaming for live simulation updates
- GPU-accelerated integration via CuPy
