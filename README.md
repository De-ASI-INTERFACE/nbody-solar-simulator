# 🌌 N-Body Solar System Simulator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Dash](https://img.shields.io/badge/Dash-2.x-green)](https://dash.plotly.com)
[![SciPy](https://img.shields.io/badge/SciPy-ODE-orange)](https://scipy.org)
[![NASA JPL](https://img.shields.io/badge/NASA-JPL%20Horizons-red)](https://ssd.jpl.nasa.gov/horizons/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-grade, interactive N-body gravitational simulator for our solar system, featuring:

- **Real-time Dash UI** — Interactive Plotly 3D orbital visualization with live controls
- **SciPy ODE Integration** — RK45 adaptive Runge-Kutta integrator for accurate gravitational dynamics
- **NASA JPL Horizons Ephemeris** — Live initial conditions fetched directly from JPL's HORIZONS API
- **Real-Time Orbital Mechanics** — Full Newtonian gravity with configurable timestep and body selection
- **Multi-Body Support** — Sun + all 8 planets + configurable dwarf planets and moons

## Architecture

```
nbody-solar-simulator/
├── app.py                    # Dash application entry point
├── simulator/
│   ├── __init__.py
│   ├── nbody.py              # SciPy RK45 ODE integrator
│   ├── ephemeris.py          # NASA JPL Horizons API client
│   └── bodies.py             # Celestial body data models
├── assets/
│   └── style.css             # Dash UI theming
├── requirements.txt
├── CHANGELOG.md
└── README.md
```

## Installation

```bash
git clone https://github.com/De-ASI-INTERFACE/nbody-solar-simulator.git
cd nbody-solar-simulator
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Open your browser to `http://localhost:8050`. The simulator will:
1. Query NASA JPL Horizons for current planetary positions and velocities
2. Initialize the N-body ODE system with live ephemeris data
3. Integrate forward using SciPy's RK45 solver
4. Render real-time 3D orbital trajectories in the Dash interface

## Configuration

Edit `simulator/bodies.py` to add/remove celestial bodies. Adjust integration parameters in `simulator/nbody.py`:

```python
INTEGRATOR_CONFIG = {
    'method': 'RK45',
    'rtol': 1e-8,
    'atol': 1e-10,
    'max_step': 3600.0,  # seconds
}
```

## Data Source

Position and velocity vectors are fetched from the [NASA JPL HORIZONS System](https://ssd.jpl.nasa.gov/horizons/) via its REST API. Ephemeris data is in the J2000.0 ecliptic reference frame.

## Physics Model

The simulator solves the coupled N-body gravitational ODE system:

```
d²rᵢ/dt² = G * Σⱼ≠ᵢ mⱼ(rⱼ - rᵢ) / |rⱼ - rᵢ|³
```

Using SciPy's `solve_ivp` with the RK45 adaptive step method for energy conservation and accuracy.

## License

MIT License — see [LICENSE](LICENSE)

## Author

**Richard Patterson** — [@De-ASI-INTERFACE](https://github.com/De-ASI-INTERFACE)
