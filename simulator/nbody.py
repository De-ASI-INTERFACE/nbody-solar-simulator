"""N-Body gravitational ODE integrator using SciPy RK45."""

import io
import csv
import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, List
from simulator.bodies import GRAVITATIONAL_CONSTANT, AU_TO_METERS, DAY_TO_SECONDS

INTEGRATOR_CONFIG = {
    "method": "RK45",
    "rtol": 1e-8,
    "atol": 1e-10,
    "max_step": 3600.0,
    "dense_output": False,
}

OUTPUT_STEPS = 500


def integrate_nbody(ephem_data: Dict[str, dict], duration_days: float) -> Dict[str, List[List[float]]]:
    body_names = list(ephem_data.keys())
    n = len(body_names)
    masses = np.array([ephem_data[b]["mass"] for b in body_names])

    positions_m = np.array([[c * AU_TO_METERS for c in ephem_data[b]["pos"]] for b in body_names])
    velocities_ms = np.array([[c * AU_TO_METERS / DAY_TO_SECONDS for c in ephem_data[b]["vel"]] for b in body_names])

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
                if r_mag < 1e6:
                    r_mag = 1e6
                acc[i] += GRAVITATIONAL_CONSTANT * masses[j] * r_vec / r_mag**3
        return np.concatenate([vel.flatten(), acc.flatten()])

    sol = solve_ivp(equations, t_span, y0, t_eval=t_eval, **INTEGRATOR_CONFIG)
    if not sol.success:
        raise RuntimeError(f"ODE integration failed: {sol.message}")

    trajectories = {}
    for i, name in enumerate(body_names):
        xs = sol.y[3*i, :] / AU_TO_METERS
        ys = sol.y[3*i+1, :] / AU_TO_METERS
        zs = sol.y[3*i+2, :] / AU_TO_METERS
        trajectories[name] = list(zip(xs.tolist(), ys.tolist(), zs.tolist()))
    return trajectories


def compute_energy_diagnostics(ephem_data: Dict[str, dict], trajectories: Dict[str, List[List[float]]], duration_days: float):
    body_names = list(ephem_data.keys())
    diagnostics = []
    for body in body_names:
        traj = np.array(trajectories[body])
        radius_au = float(np.mean(np.linalg.norm(traj, axis=1)))
        min_radius_au = float(np.min(np.linalg.norm(traj, axis=1)))
        max_radius_au = float(np.max(np.linalg.norm(traj, axis=1)))
        diagnostics.append({
            "body": body,
            "avg_radius_au": round(radius_au, 6),
            "min_radius_au": round(min_radius_au, 6),
            "max_radius_au": round(max_radius_au, 6),
            "duration_days": duration_days,
            "samples": len(traj),
        })
    return diagnostics


def export_trajectories_csv(trajectories: Dict[str, List[List[float]]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["body", "frame", "x_au", "y_au", "z_au"])
    for body, points in trajectories.items():
        for i, (x, y, z) in enumerate(points):
            writer.writerow([body, i, x, y, z])
    return buffer.getvalue()
