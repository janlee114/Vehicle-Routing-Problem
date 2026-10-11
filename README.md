# Vehicle Routing Problem: Metaheuristic Visualizations

This repository contains standalone Python/Pygame demonstrations of metaheuristic and search-based methods for constructing and visualizing customer-visiting routes.

Each script is an independent interactive application. Place customer locations on a grid, start the selected algorithm, and observe the current best route and its distance.

> **Scope:** The inspected scripts model a depot and a single tour that visits each customer and returns to the depot. This is a single-tour routing model, not a full capacitated, multi-vehicle VRP. Vehicle capacities, demands, time windows, and road-network travel costs should not be assumed unless a script explicitly implements them.

## Features

- Interactive customer placement by left-clicking.
- Grid-snapped coordinates and a fixed depot at the center of the window.
- Animated route visualization during optimization.
- Iteration or generation and best-distance display.
- Final route and distance printed to the terminal.
- Separate scripts for experimenting with different search strategies.

## Requirements

- Python 3.9 or later recommended.
- Pygame.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

If you prefer, install Pygame directly with `python -m pip install pygame`.

## Run a script

From a terminal opened in the repository directory, run a selected file. For example:

```bash
python "VRP using GA.py"
```

Or run Ant Colony Optimization:

```bash
python "VRP using ACO.py"
```

1. Left-click inside the grid to add customer locations. The depot is already placed at the center.
2. Press **Enter** to begin the selected algorithm.
3. Observe the route and best-distance display as the search progresses.
4. Read the final route and distance printed in the terminal.
5. Close the Pygame window to exit.

Keep quotation marks around filenames that contain spaces.

## Algorithm catalog

The repository contains many independent implementations. See **[ALGORITHMS.md](ALGORITHMS.md)** for the full filename catalog. The abbreviations in filenames identify the scripts; where an acronym may refer to multiple variants in the literature, consult the script's window title, comments, parameters, and operators rather than assuming a canonical expansion.

## Route representation and objective

Customer locations are stored as two-dimensional coordinates. In the inspected examples, route length is computed using Euclidean distance between consecutive points. For a customer order `[c1, c2, ..., cn]`, the evaluated tour is:

```text
[depot, c1, c2, ..., cn, depot]
```

The objective is to minimize the sum of distances along the tour while visiting every customer once. The implementation details and search operators differ by script.

## Configuration

Parameters are defined near the top of each Python file. Depending on the method, they may include population size, iteration or generation limits, mutation rate, pheromone settings, or method-specific exploration controls. Edit the constants in the selected script to change its configuration.

## Repository structure

```text
Vehicle-Routing-Problem/
├── README.md
├── ALGORITHMS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE.md
├── requirements.txt
├── .gitattributes
└── VRP using <ALGORITHM>.py
```

The scripts are standalone programs; the current repository layout does not provide a shared launcher or common configuration module.

## Limitations and research use

- Distances in the inspected scripts are Euclidean, not road-network distance or travel time.
- The inspected examples use a single depot and a single tour.
- Metaheuristics are stochastic; results may vary between runs.
- A best-so-far solution is not a proof of global optimality.
- Parameter choices and implementation details differ across files.
- For a fair comparison, use identical customer coordinates, document parameters and stopping conditions, repeat stochastic runs, and report suitable summary statistics. Do not conclude that one method is superior from a single run.

These demos are intended for learning, experimentation, and prototyping. Verify the selected script before using it as a research implementation of a particular algorithm variant.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on adding algorithms, documenting implementation details, and reporting comparisons. Project-level documentation changes are recorded in [CHANGELOG.md](CHANGELOG.md).

## License

No reuse license has been selected yet. See [LICENSE.md](LICENSE.md) for the current status. Unless a license is added, do not assume the code is available for unrestricted reuse or redistribution.
