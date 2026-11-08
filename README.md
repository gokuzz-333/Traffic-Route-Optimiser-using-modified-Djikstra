# Adaptive Traffic Route Optimizer Using Modified Dijkstra Algorithm

## 1. Project overview
This beginner-friendly Python project models a small city as a weighted graph.
It compares:

- **Standard Dijkstra:** selects the route with the smallest total road distance.
- **Modified Dijkstra:** selects the route with the smallest current travel time,
  considering traffic congestion and road penalties.

It also simulates changing traffic and re-routes a vehicle from its current
intersection when a faster route becomes available.

## 2. Requirements
- Python 3.10 or newer
- NetworkX
- Matplotlib

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 3. Run the project

Open a terminal in this folder and run:

```bash
python main.py
```

The program prints the route and comparison results, simulates vehicle movement,
and opens Matplotlib graph windows. Close each graph window to continue.

## 4. Project files

| File | Purpose |
|---|---|
| `main.py` | Runs the complete project and prints results |
| `graph_builder.py` | Creates the sample city road network |
| `traffic.py` | Simulates congestion and calculates travel time |
| `algorithms.py` | Contains Standard and Modified Dijkstra |
| `visualizer.py` | Draws traffic levels and selected routes |
| `requirements.txt` | Lists required Python packages |

## 5. Travel-time formula

The report's formula is:

`weight = distance / (speed_limit * (1 - congestion)) + penalty`

In this implementation, distance is measured in kilometres and speed in km/hour.
Therefore, the travel time is converted from hours to minutes:

`travel_time_minutes = (distance / effective_speed) * 60 + penalty`

where:

`effective_speed = speed_limit * (1 - congestion)`

Congestion is a value from 0 to less than 1. A closed road has infinite travel
time, so Modified Dijkstra skips it. Penalty is measured in minutes.

## 6. How re-routing works
1. The vehicle starts at the source intersection.
2. It moves one road at a time along the current fastest route.
3. At a fixed interval, simulated congestion values are updated.
4. Modified Dijkstra runs again from the vehicle's current intersection.
5. If the new route has a lower remaining travel time, the vehicle switches.

The demonstration has a bounded number of movement steps so it always finishes.
Traffic updates use a fixed random seed in the demo, so the same run produces
the same sequence of traffic changes. If an updated route contains a closed
road, the vehicle recalculates a route from its current intersection before
moving again.

Road data is checked before it is used. Distances and penalties must be
nonnegative, speed limits must be positive, and congestion must be between 0
and 1. Fully congested or explicitly closed roads are treated as unavailable.

## 7. Important project limitation
Traffic is simulated; this version does not connect to a live traffic service.
The sample road network and its coordinates are illustrative, not a real city map.
Traffic is treated as fixed during each individual Dijkstra run.

## 8. Complexity
With an adjacency-list graph and min-heap, each Dijkstra run has time complexity
`O((V + E) log V)` and graph storage uses `O(V + E)` space. Re-routing runs the
Modified Dijkstra algorithm again after each traffic update.
