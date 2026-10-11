# Algorithm File Catalog

This catalog lists the Python scripts present in the repository and records the expansion used in each script where the source itself provides a clear label. An acronym alone is not always enough to identify a unique algorithm in the literature; ambiguous names are marked for source-level verification instead of being expanded by guesswork.

All files are separate Pygame applications unless their implementation is changed in a future revision. Most share a common interaction pattern: add customers on a grid, press Enter, and observe a route-search process.

| Script | Name or identification | Notes |
|---|---|---|
| `VRP using ABA.py` | Artificial Beehive Algorithm (ABA) | The window title identifies this expansion. |
| `VRP using ABFTO.py` | ABFTO | Verify the intended full name in the source and associated reference before citing a specific variant. |
| `VRP using ABO.py` | ABO | Acronym retained; verify the intended variant. |
| `VRP using ABOA.py` | ABOA | Acronym retained; verify the intended variant. |
| `VRP using ACO.py` | Ant Colony Optimization (ACO) | Pheromone-based route construction. |
| `VRP using AF-CHSA.py` | AF-CHSA | Compound acronym; verify its intended expansion. |
| `VRP using AFA.py` | AFA | Verify the intended expansion. |
| `VRP using AFSA.py` | AFSA | Verify the intended expansion. |
| `VRP using ALSO.py` | ALSO | Verify the intended expansion. |
| `VRP using AMO.py` | AMO | Verify the intended expansion. |
| `VRP using ASI.py` | ASI | Verify the intended expansion. |
| `VRP using AWDA.py` | AWDA | Verify the intended expansion. |
| `VRP using BCO.py` | BCO | Verify the intended variant. |
| `VRP using BCO2.py` | BCO2 | Verify the intended variant. |
| `VRP using BNMRA.py` | BNMRA | Verify the intended expansion. |
| `VRP using BO.py` | BO | Verify the intended expansion. |
| `VRP using BROA.py` | BROA | Verify the intended expansion. |
| `VRP using BTA.py` | BTA | Verify the intended expansion. |
| `VRP using BWOA.py` | BWOA | Verify the intended expansion. |
| `VRP using CA.py` | CA | Verify the intended variant. |
| `VRP using CCA.py` | CCA | Verify the intended variant. |
| `VRP using CDOA.py` | CDOA | Verify the intended expansion. |
| `VRP using COA.py` | COA | Verify the intended expansion. |
| `VRP using COFA.py` | COFA | Verify the intended expansion. |
| `VRP using CSO.py` | CSO | Verify the intended variant. |
| `VRP using CVO.py` | CVO | Verify the intended expansion. |
| `VRP using DA.py` | DA | Verify the intended variant. |
| `VRP using DGO.py` | DGO | Verify the intended expansion. |
| `VRP using DPO.py` | DPO | Verify the intended expansion. |
| `VRP using DSO.py` | DSO | Verify the intended expansion. |
| `VRP using EFO.py` | EFO | Verify the intended expansion. |
| `VRP using EPCA.py` | EPCA | Verify the intended expansion. |
| `VRP using ESWSA.py` | ESWSA | Verify the intended expansion. |
| `VRP using FCIA.py` | FCIA | Verify the intended expansion. |
| `VRP using FDA.py` | FDA | Verify the intended expansion. |
| `VRP using FGA.py` | FGA | Verify the intended expansion. |
| `VRP using FIFAWC.py` | FIFAWC | Verify the intended expansion. |
| `VRP using GA.py` | Genetic Algorithm (GA) | Evolutionary search with selection, crossover, and mutation. |
| `VRP using GBA.py` | GBA | Verify the intended expansion. |
| `VRP using GNA.py` | GNA | Verify the intended expansion. |
| `VRP using GTO.py` | GTO | Verify the intended expansion. |
| `VRP using HBIA.py` | HBIA | Verify the intended expansion. |
| `VRP using IWDA.py` | IWDA | Verify the intended expansion. |
| `VRP using KHA.py` | KHA | Verify the intended expansion. |
| `VRP using KMA.py` | KMA | Verify the intended expansion. |
| `VRP using LSO.py` | LSO | Verify the intended expansion. |
| `VRP using MATCO.py` | MATCO | Verify the intended expansion. |
| `VRP using MRO.py` | MRO | Verify the intended expansion. |
| `VRP using NPO.py` | NPO | Verify the intended expansion. |
| `VRP using PIO.py` | PIO | Verify the intended expansion. |
| `VRP using POPMUSIC.py` | POPMUSIC | Verify the intended expansion and exact implementation variant. |
| `VRP using PPA.py` | PPA | Verify the intended expansion. |
| `VRP using PSO.py` | Penguin Search Optimization (PeSOA) | The script's Pygame title identifies it as a penguin-search method, not the conventional Particle Swarm Optimization acronym. |
| `VRP using QSA.py` | QSA | Verify the intended expansion. |
| `VRP using RFD.py` | RFD | Verify the intended expansion. |
| `VRP using RIO.py` | RIO | Verify the intended expansion. |
| `VRP using ROA.py` | ROA | Verify the intended expansion. |
| `VRP using RTGBO.py` | RTGBO | Verify the intended expansion. |
| `VRP using SA.py` | SA | Verify the intended variant. |
| `VRP using SARO.py` | SARO | Verify the intended expansion. |
| `VRP using SGO.py` | SGO | Verify the intended expansion. |
| `VRP using SHO.py` | SHO | Verify the intended expansion. |
| `VRP using SLCA.py` | SLCA | Verify the intended expansion. |
| `VRP using SM3-MBO.py` | SM3-MBO | Compound acronym; verify the intended expansion. |
| `VRP using SMO.py` | SMO | Verify the intended variant. |
| `VRP using SWOA.py` | SWOA | Verify the intended expansion. |
| `VRP using TCO.py` | TCO | Verify the intended expansion. |
| `VRP using TPA.py` | TPA | Verify the intended expansion. |
| `VRP using TSA.py` | TSA | Verify the intended variant. |
| `VRP using TSA2.py` | Tree-Seed Algorithm | The Pygame title identifies this file as a tree-seed implementation. |
| `VRP using TTA.py` | TTA | Verify the intended expansion. |
| `VRP using VND.py` | Variable Neighborhood Descent (VND) | Uses swap, 2-opt, and insertion neighborhoods. |
| `VRP using WSA.py` | WSA | Verify the intended expansion. |
| `VRP using WSO.py` | Wasp Swarm Optimization (WSO) | The Pygame title identifies this expansion. |
| `VRP using WVO.py` | WVO | Verify the intended expansion. |

## How to interpret this catalog

- The file list above reflects the repository root reviewed for this document; update the catalog when scripts are added, renamed, or removed.
- A filename is not proof that the code implements every operator from a published algorithm. Compare the source with the intended primary reference before making a research claim.
- Some names are overloaded across research fields. Confirm each ambiguous expansion with the implementation author or a citable source rather than inferring it from the acronym.
- A script that uses an algorithm-inspired heuristic should be described as an implementation or adaptation unless its fidelity to the published method has been validated.
- The shared interface and distance objective do not by themselves establish that all implementations have equivalent constraints, operators, stopping criteria, or solution quality.

## Suggested metadata for future entries

For a more rigorous algorithm inventory, add these fields for each script: canonical algorithm name, source/reference, original publication year, search representation, initialization, exploration operators, exploitation operators, acceptance/replacement rule, stopping criterion, and validation status.
