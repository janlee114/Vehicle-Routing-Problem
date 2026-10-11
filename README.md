# Vehicle Routing Problem: Metaheuristic Visualizations

This repository contains standalone Python implementations of metaheuristic and optimization algorithms for constructing and visualizing customer-visiting routes on a grid.

Each script provides a small interactive **Pygame** application. You place customer locations with the mouse, run the selected algorithm, and watch its current best route and distance update during the search.

> **Model scope:** The scripts inspected in this repository represent one depot and one route that visits every customer and returns to the depot. They are useful for studying route-order optimization, which is a single-tour form of the routing problem. Vehicle capacities, multiple vehicles, time windows, and customer demands are not represented in these implementations unless a particular script explicitly adds them.

## Features

- Interactive customer placement with left-click.
- Grid-snapped coordinates for repeatable, easy-to-read layouts.
- A fixed depot at the center of the application window.
- Animated route visualization while the selected search algorithm runs.
- A running display of the iteration or generation and best route distance.
- Final route and total distance printed to the terminal.
- Separate scripts so algorithms can be run and studied independently.

## Requirements

- Python 3.9 or later recommended.
- Pygame.

Install Pygame:

```bash
python -m pip install pygame
```

## Run an algorithm

1. Clone or download this repository.
2. Open a terminal in the repository directory.
3. Run one of the Python scripts, for example:

   ```bash
   python "VRP using GA.py"
   ```

   Or run Ant Colony Optimization:

   ```bash
   python "VRP using ACO.py"
   ```

4. In the Pygame window, left-click inside the grid to add customer locations. Each click adds a customer; the depot is already placed at the center.
5. Press **Enter** to start the algorithm.
6. Observe the route and best-distance display. The final route and distance are also printed in the terminal.
7. Close the Pygame window when you are finished.

Because filenames contain spaces, keep the quotation marks around the filename when running a script from a terminal.

## Algorithm implementations

Each algorithm is provided as a separate file named `VRP using NAME.py`. The repository includes implementations such as:

- **Ant Colony Optimization (ACO)** — `VRP using ACO.py`
- **Genetic Algorithm (GA)** — `VRP using GA.py`
- **Artificial Beehive Algorithm (ABA)** — `VRP using ABA.py`
- Additional population-based, swarm-inspired, evolutionary, and local-search methods, each in its own Python file.

The filename is the most reliable way to identify the implementation. Algorithm abbreviations can have different expansions in the literature, so consult the corresponding script before assuming a particular variant.

## How the route is evaluated

In the inspected implementations, customer locations are represented by two-dimensional coordinates. Route length is calculated using Euclidean distance between consecutive points. If the customer visit order is

`[c_1, c_2, \ldots, c_n]`,

the complete tour is

`[depot, c_1, c_2, \ldots, c_n, depot]`.

The objective is to minimize the sum of distances along that tour. Every customer is intended to be visited once before returning to the depot.

The algorithms use different search strategies and parameter settings. Consequently, their results and runtime can differ. A single run does not establish that one algorithm is generally superior; fair comparisons should use the same customer coordinates, multiple random seeds or repeated trials, and clearly stated evaluation criteria.

## Configuration

Search parameters are defined near the top of each script. Depending on the algorithm, these may include population size, number of iterations or generations, mutation rate, pheromone influence, evaporation rate, and other algorithm-specific controls. Edit the relevant script's constants to change its search settings.

The display grid and window dimensions are also configured in the script.

## Repository organization

```text
Vehicle-Routing-Problem/
├── README.md
├── .gitattributes
└── VRP using <ALGORITHM>.py
```

The Python files are independent demos; there is no single launcher or shared configuration file in the current layout.

## Limitations and interpretation

- The route distance is based on straight-line Euclidean distance, not real road-network travel distance or travel time.
- The visualizer models one depot and a single tour in the inspected scripts.
- A stochastic metaheuristic may produce different results on different runs.
- The displayed best distance is an optimization result for the generated coordinate layout, not a guarantee of a globally optimal solution.
- Parameters and implementation details differ between scripts; inspect the selected file for its exact behavior.

## Suggested use

These examples can support classroom demonstrations, algorithm prototyping, and controlled comparisons of metaheuristic search strategies. For research comparisons, document the instance coordinates, parameter settings, stopping criteria, repeat count, and performance measures.

## License

No license information was identified in the repository root at the time this README was revised. Unless a license is added, do not assume that the code is available for unrestricted reuse or redistribution.
