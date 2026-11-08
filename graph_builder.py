"""Create a small example city road network using NetworkX."""
import networkx as nx

DEFAULT_SOURCE = "A"
DEFAULT_DESTINATION = "H"


def add_road(graph, start, end, distance, speed, congestion,
             capacity=1000, penalty=0.0, closed=False):
    """Add a two-way road and store its properties."""
    attributes = {
        "distance": float(distance),       # kilometres
        "speed_limit": float(speed),       # kilometres per hour
        "congestion": float(congestion),   # value from 0.0 to 1.0
        "capacity": int(capacity),         # illustrative vehicles/hour
        "penalty": float(penalty),         # minutes: signal/accident delay
        "closed": bool(closed),
    }
    graph.add_edge(start, end, **attributes)


def build_city_graph():
    """
    Build a sample road network.
    The coordinates are illustrative positions for drawing, not GPS locations.
    """
    graph = nx.Graph()

    positions = {
        "A": (0, 2), "B": (1, 3), "C": (1, 1), "D": (2, 2),
        "E": (3, 3), "F": (3, 1), "G": (4, 2), "H": (5, 2),
    }
    for node, position in positions.items():
        graph.add_node(node, pos=position)

    # A shorter central route can become slower when its congestion is high.
    add_road(graph, "A", "B", 2.0, 50, 0.15, penalty=0.2)
    add_road(graph, "A", "C", 2.2, 55, 0.10)
    add_road(graph, "B", "D", 1.8, 45, 0.75, penalty=0.5)
    add_road(graph, "C", "D", 1.7, 50, 0.20)
    add_road(graph, "B", "E", 2.4, 60, 0.10)
    add_road(graph, "D", "E", 1.5, 40, 0.80, penalty=0.4)
    add_road(graph, "D", "F", 2.0, 55, 0.15)
    add_road(graph, "C", "F", 2.8, 60, 0.10)
    add_road(graph, "E", "G", 1.8, 50, 0.20)
    add_road(graph, "F", "G", 1.6, 45, 0.15)
    add_road(graph, "G", "H", 2.0, 60, 0.10)
    add_road(graph, "E", "H", 4.0, 65, 0.05)

    return graph
