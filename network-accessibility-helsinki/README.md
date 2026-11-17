# Network accessibility in Helsinki

Course project for Design in Networked Systems (TU Delft, MSc CoSEM). The notebook looks at how accessible parts of Helsinki are, using the city's districts and transport network.

## What the notebook does

- Reads district and transport-network shapefiles with geopandas and plots them together, with the district index numbers on the map.
- Loads the adjacency matrices of the selected districts and turns them into networkx graphs.
- Computes betweenness centrality per node and draws the networks on their real coordinates, with node size proportional to centrality, to show which nodes carry the most routes.

## What I learned

- **Combining spatial and network data.** A map (geometry) and a network (connections) describe the same city in different ways; the useful part is plotting one on top of the other.
- **Centrality as an accessibility argument.** Betweenness centrality points to the nodes that many shortest routes pass through, which is where a disruption would hurt most.
- **Working with files that come with a course project.** Shapefiles, text matrices and coordinate dictionaries have to be loaded and matched up before any analysis is possible.

The shapefiles and adjacency matrices belong to the course and are not included, so the notebook will not run without them.
