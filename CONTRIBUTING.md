# Contributing

Thank you for your interest in improving the Vehicle Routing Problem demonstrations.

## Scope

Contributions may include new algorithm implementations, corrections to existing search operators, visualization improvements, reproducibility improvements, and documentation updates. Keep each algorithm demo independently runnable unless a repository-wide refactor is proposed and documented.

## Before submitting a change

1. Identify the algorithm and the primary reference that describes the variant being implemented.
2. State whether the code is a direct implementation, an adaptation, or an algorithm-inspired heuristic.
3. Preserve the route representation and interaction pattern where practical, or document any intentional differences.
4. Avoid describing the single-tour demo as a capacitated or multi-vehicle VRP unless the corresponding constraints are implemented.
5. Keep dependencies explicit and avoid adding packages that are not needed.

## Algorithm implementation checklist

- [ ] The route contains every customer exactly once.
- [ ] The depot is excluded from the customer permutation and is added at both ends when evaluating the tour.
- [ ] The objective calculation includes the final return to the depot.
- [ ] Candidate-generation operators preserve a valid permutation or repair it deterministically.
- [ ] Edge cases are considered, including zero or one customer and routes too short for a neighborhood operator.
- [ ] The best-so-far solution is retained when that is the intended behavior.
- [ ] The GUI responds to close events and does not continue an optimization after the user exits.
- [ ] Algorithm-specific parameters are documented near their definitions.
- [ ] The final route and objective value are reported clearly.

## Validation and comparisons

When comparing algorithms, use the same customer coordinates and distance function. For stochastic algorithms, perform repeated runs with recorded random seeds where supported. Report the parameter settings, stopping budget, number of customers, best and typical objective values, runtime measurement method, and any failed or invalid runs.

Do not claim statistical superiority based on one run. For research use, select suitable statistical procedures and report uncertainty or variability.

## Documentation expectations

For each new or substantially revised script, update `ALGORITHMS.md` and, when needed, `README.md`. Include:

- The canonical name and acronym.
- A primary citation or project reference, when available.
- The representation of a candidate solution.
- The objective function and constraints.
- The initialization and principal search operators.
- Parameters and stopping conditions.
- Known limitations and how the implementation differs from the reference.

Do not invent citations or expand an ambiguous acronym without evidence.

## Pull request checklist

- [ ] The script starts with the documented command.
- [ ] The GUI can be closed normally.
- [ ] The route representation and distance calculation are valid for the intended instance.
- [ ] New dependencies are reflected in `requirements.txt`.
- [ ] Documentation matches the actual code.
- [ ] Claims about optimality, speed, or superiority are supported by appropriate evidence.

Please keep changes focused and describe what was changed, why it was needed, and how it was checked.
