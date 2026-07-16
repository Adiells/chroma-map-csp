# Map Coloring CSP Solver

This repository implements the classic map coloring algorithm as a Constraint Satisfaction Problem (CSP) for an introductory Artificial Intelligence course. It converts geographic boundaries into a mathematical topology graph and applies backtracking search to ensure no adjacent states share the same color.

## 👥 Team Members
* Adiel Emilson
* Carlos Adauto
* Guilherme Rocha
* Ricardo Pistori

## 🚀 Getting Started

Once you have generated and saved the initial spatial graph layout, you can load it instantly in your scripts using `networkx` without reprocessing the original geographic files.

### Loading the Graph

```python
import networkx as nx

# Load the graph directly from the file
G = nx.read_gexf("data/grafo_brasil.gexf")

# Reconstruct the positions dictionary (pos) from the saved attributes
pos = {node: (G.nodes[node]['x'], G.nodes[node]['y']) for node in G.nodes()}

print(f"Grafo carregado! Nós: {len(G.nodes)}, Arestas: {len(G.edges)}")
