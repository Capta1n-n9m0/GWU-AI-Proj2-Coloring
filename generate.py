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
  nodes_space: npt.NDArray[int] = np.arange(10, 60, 1)
  p_space: npt.NDArray[float] = np.arange(0.05, 0.50, 0.05)
  
  unique = generate_average_colors(nodes_space, p_space)
  
  plt.figure(figsize=(20, 20))
  draw_average_colors(unique, nodes_space, p_space)
  

  
  

if __name__ == "__main__":
  main()
  