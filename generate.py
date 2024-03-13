import networkx as nx
import networkx.generators as nxgen
import numpy as np
import numpy.typing as npt
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from typing import Callable

Gnp_generator = Callable[[int, float], nx.Graph]
Gnm_generator = Callable[[int, int], nx.Graph]

def get_average_of_n_graphs(n: int, nodes: int, p: float) -> float:
  average_n_colors = 0
  for _ in range(n):
    g: nx.Graph = nxgen.fast_gnp_random_graph(nodes, p)
    average_n_colors += max(nx.coloring.greedy_color(g, strategy='largest_first').values()) + 1
  return average_n_colors / n


def generate_average_colors(nodes_space: npt.NDArray[int], p_space: npt.NDArray[float]):
  average_colors = np.zeros((len(nodes_space), len(p_space)))
  nodes: int | None = None
  p: float | None = None
  try:
    for i, nodes in enumerate(nodes_space):
      print(f"nodes: {nodes}")
      for j, p in enumerate(p_space):
        average_colors[i, j] = get_average_of_n_graphs(100, nodes, p)
  except KeyboardInterrupt:
    print(f"Interrupted at nodes: {nodes}, p: {p}")
  
  unique = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  filename = f"average_colors_{unique}.npy"
  np.save(filename, average_colors)
  return unique


def draw_average_colors(unique: str, nodes_space: npt.NDArray[int], p_space: npt.NDArray[float]):
  average_colors = np.load(f"average_colors_{unique}.npy")
  
  # heatmap of average colors with number of colors printed in each cell
  sns.heatmap(average_colors, annot=True, fmt=".2f", xticklabels=p_space, yticklabels=nodes_space)
  
  plt.savefig(f"average_colors_{unique}.png")

def main():
  N = 5000
  P = 0.10
  g = nxgen.fast_gnp_random_graph(N, P)
  colors = nx.coloring.greedy_color(g, strategy='largest_first')
  n_colors = max(colors.values()) + 1
  with open("input-11.txt", "w") as file:
    file.write(f"# Graph with {len(g.nodes)} nodes and {len(g.edges)} edges\n")
    file.write(f"# Generated with fast_gnp_random_graph({N}, {P})\n")
    file.write(f"# Generated on {datetime.datetime.now()}\n")
    file.write(f"colors = {n_colors}\n")
    for edge in g.edges:
      file.write(f"{edge[0]},{edge[1]}\n")
  

  
  

if __name__ == "__main__":
  main()
  