# Graph theory and decision analysis (TU Delft BSc, Besliskunde)

Three Python assignments in Dutch, all built around one story: finding and sharing a student house. The tools are networkx and matplotlib. Assignments 2B and 3 are worked out; 1A contains the set-up only.

| Assignment | Problem | Method |
|---|---|---|
| `assignment-1a-shortest-paths` | Which of the offered student rooms is the most central, and how does that change when you cycle to some locations more often than to others? | Weighted street graph with rooms, locations and crossings. In this copy only the graph set-up is included; the answer cells are empty |
| `assignment-2b-bipartite-matching` | Divide the weekly cleaning jobs over housemates, then redo it when people refuse certain jobs (dust allergy, dirty toilets) | Bipartite graph; solved as a maximum flow problem and with a maximum matching |
| `assignment-3-routes-and-euler-circuits` | Plan a route that passes through all the places of interest | All-pairs shortest path lengths (Dijkstra), exhaustive search over all orderings of ten nodes, and an Euler circuit check |

## What I learned

- **Modelling is the hard part.** A housing question or a chore rota only becomes solvable once it is written as a graph: what are the nodes, what are the edges, what do the weights mean.
- **The same problem has several algorithms.** Matching can be solved with a flow formulation or with a dedicated matching function, and both give the same answer.
- **Constraints change the model, not just the answer.** When a housemate refuses a job, an edge disappears from the graph and the solution has to be recomputed.
- **Brute force has a limit.** Trying every ordering of ten places works (10! is about 3.6 million), but it grows factorially, which is why heuristics and better algorithms exist.
