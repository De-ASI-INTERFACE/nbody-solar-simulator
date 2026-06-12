"""N-Body gravitational ODE integrator using SciPy RK45.

Solves the coupled Newtonian gravitational equations:
    d²rᵢ/dt² = G * Σⱼ≠ᵢ mⱼ(rⱼ - rᵢ) / |rⱼ - rᵢ|³

State vector layout: [x0,y0,z0, x1,y1,z1, ..., vx0,vy0,vz0, vx1,vy1,vz1, ...]
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, List
from simulator.bodies import GRAVITATIONAL_CONSTANT, AU_TO_METERS, DAY_TO_SECONDS

INTEGRATOR_CONFIG = {
    "method": "RK45",
    "rtol": 1e-8,
    "atol": 1e-10,
    "max_step": 3600.0,   # seconds
    "dense_output": False,
}

OUTPUT_STEPS = 500  # number of trajectory points to return


def integrate_nbody(
    ephem_data: Dict[str, dict],
    duration_days: float,
) -> Dict[str, List[List[float]]]:
    """
    Integrate the N-body system from live ephemeris initial conditions.

    Args:
        ephem_data: Output of fetch_ephemeris — dict of {body: {pos, vel, mass}}
        duration_days: Integration duration in days

    Returns:
        Dict mapping body name -> list of [x, y, z] positions in AU
        at OUTPUT_STEPS evenly-spaced time points.
    """
    body_names = list(ephem_data.keys())
    n = len(body_names)

    masses = np.array([ephem_data[b]["mass"] for b in body_names])  # kg

    # Convert initial conditions: AU -> meters, AU/day -> m/s
    positions_m = np.array([
        [c * AU_TO_METERS for c in ephem_data[b]["pos"]] for b in body_names
    ])  # shape (n, 3)

    velocities_ms = np.array([
        [c * AU_TO_METERS / DAY_TO_SECONDS for c in ephem_data[b]["vel"]] for b in body_names
    ])  # shape (n, 3)

    y0 = np.concatenate([positions_m.flatten(), velocities_ms.flatten()])
    t_span = (0.0, duration_days * DAY_TO_SECONDS)
    t_eval = np.linspace(t_span[0], t_span[1], OUTPUT_STEPS)

    def equations(t, y):
        pos = y[:3*n].reshape(n, 3)
        vel = y[3*n:].reshape(n, 3)
        acc = np.zeros((n, 3))

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                r_vec = pos[j] - pos[i]
                r_mag = np.linalg.norm(r_vec)
                if r_mag < 1e6:  # softening: 1000 km minimum
                    r_mag = 1e6
                acc[i] += GRAVITATIONAL_CONSTANT * masses[j] * r_vec / r_mag**3

        return np.concatenate([vel.flatten(), acc.flatten()])

    sol = solve_ivp(
        equations,
        t_span,
        y0,
        t_eval=t_eval,
        **INTEGRATOR_CONFIG,
    )

    if not sol.success:
        raise RuntimeError(f"ODE integration failed: {sol.message}")

    trajectories = {}
    for i, name in enumerate(body_names):
        xs = sol.y[3*i, :] / AU_TO_METERS
        ys = sol.y[3*i+1, :] / AU_TO_METERS
        zs = sol.y[3*i+2, :] / AU_TO_METERS
        trajectories[name] = list(zip(xs.tolist(), ys.tolist(), zs.tolist()))

    return trajectories
