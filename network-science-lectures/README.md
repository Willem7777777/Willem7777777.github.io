# Network science (TU Delft MSc CoSEM, Design in Networked Systems)

Exercise notebooks from the lectures, written with networkx and matplotlib. Outputs are cleared.

## `lecture-1b-graph-representations`

Exercises 1-3 are worked out: a cycle basis, vertex-induced and edge-induced subgraphs, and the strongly connected components of a directed graph, including what changes when one edge is added. Exercises 4-6 (distances in a directed graph, Dijkstra on a weighted graph, adjacency matrix and its powers) are set up, but the answer cells are empty in this copy.

## `lecture-2b-random-and-scale-free-networks`

Functions that generate a static random graph G(n, p), a dynamic random graph that adds links over a number of time steps, and a scale-free graph by preferential attachment (Barabasi-Albert). They also plot degree distributions, check connectivity and compute the average clustering coefficient, local bridges and their span, average path length and diameter.

## What I learned

- **How a network is generated shapes its structure.** A random graph has a narrow, bell-shaped degree distribution; a scale-free graph has a few hubs and many low-degree nodes.
- **Network measures answer different questions.** Clustering says how tightly neighbours are connected, path length and diameter say how far information has to travel, bridges say where a network is fragile.
- **Turning a definition into a procedure.** Most of the exercises asked me to write the generating procedure as a function and then test it with different parameters, instead of calling a library function straight away.
- **Directed graphs behave differently.** Strong connectivity depends on edge direction, and one extra edge can merge components.
