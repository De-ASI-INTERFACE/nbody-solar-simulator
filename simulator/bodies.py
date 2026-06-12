"""Celestial body definitions, NASA JPL Horizons target IDs, visual properties."""

SOLAR_BODIES = {
    "Sun":     {"horizons_id": "10",  "mass_kg": 1.989e30, "radius_km": 696340},
    "Mercury": {"horizons_id": "199", "mass_kg": 3.301e23, "radius_km": 2439.7},
    "Venus":   {"horizons_id": "299", "mass_kg": 4.867e24, "radius_km": 6051.8},
    "Earth":   {"horizons_id": "399", "mass_kg": 5.972e24, "radius_km": 6371.0},
    "Mars":    {"horizons_id": "499", "mass_kg": 6.390e23, "radius_km": 3389.5},
    "Jupiter": {"horizons_id": "599", "mass_kg": 1.898e27, "radius_km": 69911},
    "Saturn":  {"horizons_id": "699", "mass_kg": 5.683e26, "radius_km": 58232},
    "Uranus":  {"horizons_id": "799", "mass_kg": 8.681e25, "radius_km": 25362},
    "Neptune": {"horizons_id": "899", "mass_kg": 1.024e26, "radius_km": 24622},
}

BODY_COLORS = {
    "Sun":     "#FDB813",
    "Mercury": "#B5B5B5",
    "Venus":   "#E8C47A",
    "Earth":   "#4FC3F7",
    "Mars":    "#EF5350",
    "Jupiter": "#F4A460",
    "Saturn":  "#DEB887",
    "Uranus":  "#80DEEA",
    "Neptune": "#5C6BC0",
}

BODY_SIZES = {
    "Sun":     16,
    "Mercury": 4,
    "Venus":   6,
    "Earth":   6,
    "Mars":    5,
    "Jupiter": 12,
    "Saturn":  11,
    "Uranus":  8,
    "Neptune": 8,
}

GRAVITATIONAL_CONSTANT = 6.67430e-11  # m³ kg⁻¹ s⁻²
AU_TO_METERS = 1.495978707e11         # meters per AU
DAY_TO_SECONDS = 86400.0              # seconds per day
