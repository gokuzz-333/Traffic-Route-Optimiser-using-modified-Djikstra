"""Matplotlib visualizations for traffic conditions and selected routes."""
import matplotlib.pyplot as plt
import networkx as nx
from traffic import congestion_colour


def _draw_network(ax, graph, route, source, destination, title, route_colour):
    positions = nx.get_node_attributes(graph, "pos")
    route_edges = set()
    if route:
        route_edges = {frozenset((a, b)) for a, b in zip(route, route[1:])}

    edge_colours = []
    edge_widths = []
    for start, end, data in graph.edges(data=True):
        edge_colours.append(congestion_colour(
            data["congestion"], data.get("closed", False)
        ))
        edge_widths.append(4.0 if frozenset((start, end)) in route_edges else 1.5)

    nx.draw_networkx_edges(
        graph, positions, ax=ax, edge_color=edge_colours,
        width=edge_widths, alpha=0.85
    )
    nx.draw_networkx_nodes(
        graph, positions, ax=ax, node_size=850,
        node_color="#dceeff", edgecolors="#24415c", linewidths=1.5
    )
    nx.draw_networkx_labels(
        graph, positions, ax=ax, font_size=10, font_weight="bold"
    )

    if route and len(route) > 1:
        nx.draw_networkx_edges(
            graph, positions, ax=ax,
            edgelist=list(zip(route, route[1:])),
            edge_color=route_colour, width=4.5
        )

    nx.draw_networkx_nodes(
        graph, positions, ax=ax, nodelist=[source],
        node_color="#55c878", node_size=950
    )
    nx.draw_networkx_nodes(
        graph, positions, ax=ax, nodelist=[destination],
        node_color="#ff7777", node_size=950
    )

    # Display distance and congestion beside each road.
    labels = {}
    for a, b, data in graph.edges(data=True):
        labels[(a, b)] = (
            f'{data["distance"]:.1f} km\n'
            f'{data["congestion"]:.0%} jam'
        )
    nx.draw_networkx_edge_labels(
        graph, positions, edge_labels=labels, ax=ax, font_size=7
    )

    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.axis("off")


def draw_comparison(graph, standard_path, modified_path, source, destination,
                    standard_time, modified_time):
    """Show baseline and traffic-aware routes side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    _draw_network(
        axes[0], graph, standard_path, source, destination,
        f"Standard Dijkstra\nShortest-distance route\n"
        f"Current travel time: {standard_time:.2f} min",
        "#2563eb"
    )
    _draw_network(
        axes[1], graph, modified_path, source, destination,
        f"Modified Dijkstra\nFastest traffic-aware route\n"
        f"Travel time: {modified_time:.2f} min",
        "#8e44ad"
    )
    fig.suptitle(
        "Adaptive Traffic Route Optimizer\n"
        "Green = low congestion | Orange = medium | Red = high",
        fontsize=13
    )
    plt.tight_layout()
    plt.show()


def draw_reroute_history(graph, history, source, destination):
    """Show the path followed by the vehicle during the simulation."""
    fig, ax = plt.subplots(figsize=(10, 6))
    _draw_network(
        ax, graph, history, source, destination,
        "Vehicle movement during adaptive re-routing",
        "#8e44ad"
    )
    if len(history) > 1:
        ax.text(
            0.02, 0.02, "Movement: " + " -> ".join(history),
            transform=ax.transAxes, fontsize=9,
            bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "gray"}
        )
    plt.tight_layout()
    plt.show()
