"""NASA JPL Horizons REST API ephemeris client.

Fetches current Cartesian state vectors (position + velocity) for solar
system bodies in the J2000.0 ecliptic reference frame.

API docs: https://ssd-api.jpl.nasa.gov/doc/horizons.html
"""

import requests
from typing import Dict, List
from simulator.bodies import SOLAR_BODIES, AU_TO_METERS, DAY_TO_SECONDS

HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"


def fetch_ephemeris(body_names: List[str], epoch: str) -> Dict[str, dict]:
    """
    Fetch Cartesian state vectors for each body from NASA JPL Horizons.

    Args:
        body_names: List of body names (must be keys in SOLAR_BODIES)
        epoch: ISO date string YYYY-MM-DD for start epoch

    Returns:
        Dict mapping body name -> {"pos": [x,y,z] AU, "vel": [vx,vy,vz] AU/day, "mass": kg}
    """
    results = {}
    stop_epoch = epoch  # single-point query

    for name in body_names:
        if name not in SOLAR_BODIES:
            continue
        body = SOLAR_BODIES[name]
        horizons_id = body["horizons_id"]

        params = {
            "format": "json",
            "COMMAND": f"'{horizons_id}'",
            "OBJ_DATA": "NO",
            "MAKE_EPHEM": "YES",
            "EPHEM_TYPE": "VECTORS",
            "CENTER": "@0",           # Solar System Barycenter
            "START_TIME": epoch,
            "STOP_TIME": epoch,
            "STEP_SIZE": "1d",
            "VEC_TABLE": "2",          # position + velocity
            "REF_PLANE": "ECLIPTIC",
            "REF_SYSTEM": "J2000",
            "VEC_CORR": "NONE",
            "OUT_UNITS": "AU-D",       # AU and AU/day
            "CSV_FORMAT": "YES",
        }

        resp = requests.get(HORIZONS_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        pos, vel = _parse_horizons_vectors(data["result"])
        results[name] = {
            "pos": pos,
            "vel": vel,
            "mass": body["mass_kg"],
        }

    return results


def _parse_horizons_vectors(result_text: str):
    """
    Parse CSV vector output from JPL Horizons API text response.
    Returns (position [AU], velocity [AU/day]) as lists of 3 floats.
    """
    lines = result_text.split("\n")
    in_data = False
    for line in lines:
        if "$$SOE" in line:
            in_data = True
            continue
        if "$$EOE" in line:
            break
        if in_data and line.strip():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 7:
                try:
                    x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                    vx, vy, vz = float(parts[5]), float(parts[6]), float(parts[7])
                    return [x, y, z], [vx, vy, vz]
                except (ValueError, IndexError):
                    continue
    raise ValueError("Could not parse Horizons vector data from response.")
