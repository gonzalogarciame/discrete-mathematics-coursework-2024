# Practice 3: Graph Algorithms and GPS Routing

## Original Goal

The third practice applied graph theory to a GPS-style route planner. The project combines weighted graph algorithms with a Madrid street graph obtained from OpenStreetMap.

Original report: `practices/practice-3-gps-graphs/report/P3GP10A.pdf`

Source code:

- `practices/practice-3-gps-graphs/src/grafo_pesado.py`
- `practices/practice-3-gps-graphs/src/callejero.py`
- `practices/practice-3-gps-graphs/src/gps.py`

## What Was Implemented

### `grafo_pesado.py`

This module implements reusable weighted graph algorithms:

- `dijkstra(G, peso, origen)`: computes a shortest-path tree from an origin node.
- `camino_minimo(G, peso, origen, destino)`: reconstructs a shortest path from origin to destination.
- `prim(G, peso)`: computes a minimum spanning tree using Prim's algorithm.
- `kruskal(G, peso)`: computes a minimum spanning tree using Kruskal's algorithm.

The functions use NetworkX graphs and accept a custom weight function, which makes the algorithms reusable for distance, time, or any other edge cost.

### `callejero.py`

This module handles street and map utilities:

- Loads a Madrid address file named `direcciones.csv`.
- Converts latitude and longitude from degrees-minutes-seconds notation to decimal degrees.
- Searches for an address written as `"street, number"`.
- Loads a Madrid driving graph from `madrid.graphml` if available.
- Downloads and stores the graph from OpenStreetMap through OSMnx if the local file is missing.
- Converts a `MultiDiGraph` into a simpler directed graph and removes self-loops.
- Displays the graph and optionally highlights a route.

### `gps.py`

This is the main route planner. It:

- loads the street address dataset;
- loads and processes the Madrid graph;
- assigns speed limits to graph edges;
- asks for origin and destination addresses;
- finds the nearest graph vertices;
- computes the route using one of three modes;
- generates turn-by-turn style instructions;
- draws the route.

## Route Cost Functions

The GPS supports three route modes:

- Shortest route: minimizes physical distance using the edge `length`.
- Fastest route: estimates travel time using `length / speed_limit`.
- Optimized route: adds a traffic-light style penalty to the estimated travel time.

This design is a good example of why graph algorithms are powerful: Dijkstra stays the same, and only the weight function changes.

## Navigation Instructions

After computing a path, the program generates human-readable instructions. It compares consecutive street segments using vectors based on node coordinates:

- If the street name changes, it emits a new instruction.
- If the angle is small, it treats the movement as continuing straight.
- Otherwise, the determinant of the direction vectors is used to decide left or right.

Example instruction from the report:

```text
Despues de avanzar 961 metros, gira a la derecha en Calle de Cea Bermudez.
```

## How To Run

From the practice source folder:

```bash
cd practices/practice-3-gps-graphs/src
python gps.py
```

Required runtime data:

- `direcciones.csv`: Madrid address dataset.
- `madrid.graphml`: optional cached OSM graph. If absent, the program attempts to download it with OSMnx.

## Implementation Notes

The project demonstrates Dijkstra, Prim, and Kruskal in a realistic setting. It also depends on heavier geospatial packages, especially OSMnx, Pandas, NetworkX, and Matplotlib.

The original folder did not include `direcciones.csv` or `madrid.graphml`, so the full GPS workflow may require adding those files or allowing OSMnx to download the graph.
