import sys
import networkx as nx
from abc import ABC, abstractmethod


def check_coloring(graph: nx.Graph, colors: dict[int, int]) -> bool:
  for node in graph.nodes:
    for neighbor in graph.neighbors(node):
      if colors[node] == colors[neighbor]:
        return False
  return True


class Colorer(ABC):
  @abstractmethod
  def color(self) -> dict[int, int] | None:
    pass


class BuildInColorer(Colorer):
  def __init__(self, G: nx.Graph, n_colors: int):
    self.n_color = n_colors
    self.G = G.copy()
  
  def color(self) -> dict[int, int] | None:
    solution = nx.coloring.greedy_color(self.G, strategy='largest_first')
    max_color = max(solution.values())
    if max_color >= self.n_color:
      print(f"Graph has {max_color+1} colors, but {self.n_color} colors are required", file=sys.stderr)
    return solution


class NaiveBacktrackingColorer(Colorer):
  def __init__(self, G: nx.Graph, n_colors: int):
    self.n_color = n_colors
    self.G = G.copy()
  
  def color(self) -> dict[int, int] | None:
    def is_safe(graph: nx.Graph, node: int, color: int) -> bool:
      for neighbor in graph.neighbors(node):
        if graph.nodes[neighbor]['color'] == color:
          return False
      return True
  
    def graph_coloring_util(graph: nx.Graph, num_colors, node):
      uncolored_nodes = (node for node in graph.nodes if graph.nodes[node]['color'] is None)
  
      try:
        next_node = next(uncolored_nodes)
      except StopIteration:
        next_node = None
  
      if next_node is None:
        return True  # All nodes are colored
  
      for color in range(num_colors):
        if is_safe(graph, node, color):
          graph.nodes[node]['color'] = color
          if graph_coloring_util(graph, num_colors, next_node):
            return True
          graph.nodes[node]['color'] = None  # Backtrack
  
      return False  # No valid coloring found
  
    def graph_coloring(graph: nx.Graph, num_colors: int):
      try:
        first_node = next(iter(graph.nodes))
      except StopIteration:
        return {}
      for node in graph.nodes:
        graph.nodes[node]['color'] = None
      if graph_coloring_util(graph, num_colors, first_node):
        return {node: graph.nodes[node]['color'] for node in graph.nodes}
      else:
        return None  # No solution exists
  
    return graph_coloring(self.G, self.n_color)
    
