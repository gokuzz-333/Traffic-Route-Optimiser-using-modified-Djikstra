"""Standard Dijkstra and traffic-aware Modified Dijkstra."""
import heapq
import math
from traffic import calculate_travel_time


def _validate_endpoints(graph, source, destination):
    """Raise a helpful error when a requested intersection is not in the graph."""
    missing = [node for node in (source, destination) if node not in graph]
    if missing:
        names = ", ".join(repr(node) for node in dict.fromkeys(missing))
        raise ValueError(f"Unknown intersection(s): {names}")


def reconstruct_path(previous, source, destination):
    """Rebuild a route by following predecessor links backwards."""
    if source == destination:
        return [source]
    if destination not in previous:
        return []

    path = [destination]
    current = destination
    while current != source:
        current = previous.get(current)
        if current is None:
            return []
        path.append(current)
    path.reverse()
    return path


def standard_dijkstra(graph, source, destination):
    """
    Baseline Dijkstra: edge weight is fixed road distance in kilometres.
    Returns (path, total_distance_km).
    """
    _validate_endpoints(graph, source, destination)
    distances = {node: float("inf") for node in graph.nodes}
    previous = {}
    distances[source] = 0.0
    heap = [(0.0, source)]
    visited = set()

    while heap:
        current_distance, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)

        if node == destination:
            break

        for neighbour, edge in graph[node].items():
            if "distance" not in edge:
                raise ValueError(f"Road {node!r} to {neighbour!r} is missing distance")
            road_distance = float(edge["distance"])
            if not math.isfinite(road_distance) or road_distance < 0:
                raise ValueError("Road distances must be finite and nonnegative")
            new_distance = current_distance + road_distance
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = node
                heapq.heappush(heap, (new_distance, neighbour))

    if distances[destination] == float("inf"):
        return [], float("inf")
    return reconstruct_path(previous, source, destination), distances[destination]


def modified_dijkstra(graph, source, destination):
    """
    Proposed algorithm: edge weight is current traffic-aware travel time.
    Returns (path, total_travel_time_minutes).
    """
    _validate_endpoints(graph, source, destination)
    times = {node: float("inf") for node in graph.nodes}
    previous = {}
    times[source] = 0.0
    heap = [(0.0, source)]
    visited = set()

    while heap:
        current_time, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)

        if node == destination:
            break

        for neighbour, edge in graph[node].items():
            road_time = calculate_travel_time(edge)
            if road_time == float("inf"):
                continue

            new_time = current_time + road_time
            if new_time < times[neighbour]:
                times[neighbour] = new_time
                previous[neighbour] = node
                heapq.heappush(heap, (new_time, neighbour))

    if times[destination] == float("inf"):
        return [], float("inf")
    return reconstruct_path(previous, source, destination), times[destination]


def calculate_route_travel_time(graph, path):
    """Calculate current travel time along an already selected route."""
    if not path or len(path) == 1:
        return 0.0 if path else float("inf")

    total = 0.0
    for start, end in zip(path, path[1:]):
        edge_time = calculate_travel_time(graph[start][end])
        if edge_time == float("inf"):
            return float("inf")
        total += edge_time
    return total
