"""
Adaptive Traffic Route Optimizer
Run: python main.py
A beginner-friendly demonstration of Standard Dijkstra and
traffic-aware Modified Dijkstra with simulated adaptive re-routing.
"""
from time import perf_counter
import random

from graph_builder import build_city_graph, DEFAULT_SOURCE, DEFAULT_DESTINATION
from traffic import update_traffic
from algorithms import (
    standard_dijkstra,
    modified_dijkstra,
    calculate_route_travel_time,
)
from visualizer import draw_comparison, draw_reroute_history


def print_route(title, path, total, unit="minutes"):
    print(f"\n{title}")
    if not path:
        print("  No route available.")
        return
    print("  Route:", " -> ".join(path))
    print(f"  Total: {total:.2f} {unit}")


def run_comparison(graph, source, destination):
    """Compare shortest-distance and fastest-time routes on the same graph."""
    start = perf_counter()
    distance_path, distance_km = standard_dijkstra(graph, source, destination)
    standard_runtime = (perf_counter() - start) * 1000

    start = perf_counter()
    time_path, travel_minutes = modified_dijkstra(graph, source, destination)
    modified_runtime = (perf_counter() - start) * 1000

    # The standard algorithm minimizes distance, but we also calculate how
    # long that chosen route would currently take under traffic conditions.
    standard_route_minutes = calculate_route_travel_time(graph, distance_path)

    print("\n" + "=" * 64)
    print("STANDARD DIJKSTRA VS MODIFIED DIJKSTRA")
    print("=" * 64)
    print_route("1. Standard Dijkstra (minimum distance)", distance_path, distance_km, "km")
    print(f"  Current traffic time on this route: {standard_route_minutes:.2f} minutes")
    print(f"  Runtime: {standard_runtime:.4f} ms")

    print_route("2. Modified Dijkstra (minimum travel time)", time_path, travel_minutes)
    print(f"  Runtime: {modified_runtime:.4f} ms")

    print("\nComparison")
    print(f"  Distance selected by Standard Dijkstra: {distance_km:.2f} km")
    print(f"  Travel time of Standard route:           {standard_route_minutes:.2f} min")
    print(f"  Travel time of Modified route:           {travel_minutes:.2f} min")
    if standard_route_minutes > 0:
        improvement = (standard_route_minutes - travel_minutes) / standard_route_minutes * 100
        print(f"  Time saved by traffic-aware route:       {improvement:.1f}%")
    print(f"  Standard Dijkstra runtime:               {standard_runtime:.4f} ms")
    print(f"  Modified Dijkstra runtime:               {modified_runtime:.4f} ms")

    return distance_path, time_path, standard_route_minutes, travel_minutes


def simulate_adaptive_rerouting(graph, source, destination, update_every=2, steps=8,
                                seed=42):
    """
    Move a vehicle one road at a time. Every update_every steps, change
    congestion and calculate a new fastest route from the current node.
    """
    if update_every <= 0:
        raise ValueError("update_every must be greater than zero")
    if steps < 0:
        raise ValueError("steps cannot be negative")

    rng = random.Random(seed)
    current = source
    current_route, _ = modified_dijkstra(graph, current, destination)
    history = [current]
    reroute_events = []

    print("\n" + "=" * 64)
    print("ADAPTIVE RE-ROUTING SIMULATION")
    print("=" * 64)
    print(f"Vehicle starts at {source}; destination is {destination}.")
    print("Traffic is refreshed periodically using simulated congestion.")

    for step in range(1, steps + 1):
        if current == destination:
            break

        # Replan if a traffic update closed the next road on the saved route.
        if len(current_route) >= 2:
            next_edge = graph.get_edge_data(current_route[0], current_route[1])
            if (next_edge is None or next_edge.get("closed", False)
                    or calculate_route_travel_time(graph, current_route) == float("inf")):
                current_route, _ = modified_dijkstra(graph, current, destination)

        # Ensure there is a next node in the current route.
        if not current_route or len(current_route) < 2:
            print("No further route is available.")
            break

        next_node = current_route[1]
        current = next_node
        history.append(current)
        current_route = current_route[1:]
        print(f"Step {step}: vehicle moved to {current}")

        if current == destination:
            print("Destination reached.")
            break

        if step % update_every == 0:
            update_traffic(graph, seed=rng.getrandbits(32))
            new_route, new_time = modified_dijkstra(graph, current, destination)
            old_time = calculate_route_travel_time(graph, current_route)

            if new_route and (not current_route or new_time + 1e-9 < old_time):
                print(
                    f"  Traffic changed. Re-routing from {current}: "
                    f"{' -> '.join(new_route)}"
                )
                reroute_events.append((current, new_route.copy(), step))
                current_route = new_route
            else:
                print("  Traffic changed. Existing route is still the fastest.")

    if current != destination:
        # This is an intentionally bounded demonstration. It does not claim
        # the vehicle completed a trip if the step limit was reached.
        print(f"Simulation stopped at {current} (step limit reached).")
    return history, reroute_events


def main():
    print("=" * 64)
    print("ADAPTIVE TRAFFIC ROUTE OPTIMIZER")
    print("Modified Dijkstra Algorithm")
    print("=" * 64)

    graph = build_city_graph()
    source, destination = DEFAULT_SOURCE, DEFAULT_DESTINATION

    # Initial traffic values are deterministic so the demonstration is
    # repeatable. Later updates use a controlled random simulation.
    print("\nRoad network created.")
    print(f"Number of intersections: {graph.number_of_nodes()}")
    print(f"Number of roads:         {graph.number_of_edges()}")
    print(f"Source: {source} | Destination: {destination}")

    standard_path, fastest_path, standard_time, fastest_time = run_comparison(
        graph, source, destination
    )

    history, reroute_events = simulate_adaptive_rerouting(
        graph, source, destination
    )

    print("\nGenerating graph visualizations...")
    draw_comparison(
        graph, standard_path, fastest_path, source, destination,
        standard_time, fastest_time
    )
    draw_reroute_history(graph, history, source, destination)
    print("Visualization windows opened. Close them to finish the program.")


if __name__ == "__main__":
    main()
