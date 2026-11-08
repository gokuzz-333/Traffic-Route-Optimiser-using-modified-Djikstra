"""Traffic simulation and adaptive edge-weight calculation."""
import random
import math


def calculate_travel_time(edge):
    """
    Calculate road travel time in minutes.

    Formula from the project report:
      weight = distance / (speed_limit * (1 - congestion)) + penalty

    Since distance is in km and speed is in km/hour, convert hours to minutes.
    Congestion must be below 1.0. A closed road or fully blocked road has
    infinite travel time and cannot be selected by Dijkstra.
    """
    if edge.get("closed", False):
        return float("inf")

    required = ("distance", "speed_limit", "congestion")
    missing = [key for key in required if key not in edge]
    if missing:
        raise ValueError(f"Road is missing required values: {', '.join(missing)}")

    distance = float(edge["distance"])
    speed = float(edge["speed_limit"])
    congestion = float(edge["congestion"])
    penalty = float(edge.get("penalty", 0.0))

    if not all(math.isfinite(value) for value in (distance, speed, congestion, penalty)):
        raise ValueError("Road values must be finite numbers")
    if distance < 0:
        raise ValueError("Road distance cannot be negative")
    if speed <= 0:
        raise ValueError("Speed limit must be greater than zero")
    if not 0.0 <= congestion <= 1.0:
        raise ValueError("Congestion must be between 0.0 and 1.0")
    if penalty < 0:
        raise ValueError("Road penalty cannot be negative")

    if congestion == 1.0:
        return float("inf")

    effective_speed = speed * (1.0 - congestion)
    if effective_speed <= 0:
        return float("inf")

    travel_minutes = (distance / effective_speed) * 60.0
    return travel_minutes + penalty


def congestion_colour(congestion, closed=False):
    """Return a colour category for map visualization."""
    if closed:
        return "black"
    if congestion < 0.30:
        return "green"
    if congestion < 0.65:
        return "orange"
    return "red"


def update_traffic(graph, seed=None):
    """
    Simulate a new traffic snapshot.
    Values are bounded to [0.05, 0.90], so roads do not become fully blocked
    by random congestion. Closed roads remain closed.
    """
    rng = random.Random(seed) if seed is not None else random
    for _, _, data in graph.edges(data=True):
        if data.get("closed", False):
            continue
        calculate_travel_time(data)  # Validate values before updating them.
        change = rng.uniform(-0.25, 0.25)
        data["congestion"] = min(0.90, max(0.05, data["congestion"] + change))
