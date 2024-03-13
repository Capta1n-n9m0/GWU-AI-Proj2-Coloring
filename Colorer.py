import sys
import networkx as nx
from abc import ABC, abstractmethod
import timeit


def check_coloring(graph: nx.Graph, colors: dict[int, int]) -> bool:
  """
  Check if the coloring is valid. If two adjacent nodes have the same color, the coloring is invalid.
  :param graph: NetworkX graph
  :param colors: Dictionary of node-color pairs
  :return: If the coloring is valid
  """
  for node in graph.nodes:
    for neighbor in graph.neighbors(node):
      if colors[node] == colors[neighbor]:
        return False
  return True


class Colorer(ABC):
  """
  Abstract class for coloring algorithms
  
  Methods:
  __init__: Constructor
  color: Abstract method to return a valid coloring
  """
  @abstractmethod
  def __init__(self, *args, **kwargs):
    pass
  
  @abstractmethod
  def color(self) -> dict[int, int] | None:
    pass


class BuildInColorer(Colorer):
  """
  Colorer using NetworkX's greedy_color function
  """
  def __init__(self, G: nx.Graph, n_colors: int):
    self.n_color = n_colors
    self.G = G.copy()
  
  def color(self) -> dict[int, int] | None:
    solution = nx.coloring.greedy_color(self.G, strategy='largest_first')
    max_color = max(solution.values()) + 1
    if max_color > self.n_color:
      print(f"Graph has {max_color} colors, but {self.n_color} colors are required", file=sys.stderr)
    return solution


class NaiveBacktrackingColorer(Colorer):
  """
  Naive backtracking algorithm for graph coloring.
  It colors the nodes one by one, and backtracks if no valid coloring is found.
  """
  def __init__(self, G: nx.Graph, n_colors: int):
    self.n_color = n_colors
    self.G = G.copy()
  
  def is_safe(self, node: int, color: int) -> bool:
    for neighbor in self.G.neighbors(node):
      if self.G.nodes[neighbor]['color'] == color:
        return False
    return True
  
  def color_node(self, node):
    uncolored_nodes = (node for node in self.G.nodes if self.G.nodes[node]['color'] is None)
    
    try:
      next_node = next(uncolored_nodes)
    except StopIteration:
      next_node = None
    
    if next_node is None:
      return True  # All nodes are colored
    
    for color in range(self.n_color):
      if self.is_safe(node, color):
        self.G.nodes[node]['color'] = color
        if self.color_node(next_node):
          return True
        self.G.nodes[node]['color'] = None  # Backtrack
    
    return False  # No valid coloring found
  
  def color(self) -> dict[int, int] | None:
    try:
      first_node = next(iter(self.G.nodes))
    except StopIteration:
      return {}
    for node in self.G.nodes:
      self.G.nodes[node]['color'] = None
    if self.color_node(first_node):
      return {node: self.G.nodes[node]['color'] for node in self.G.nodes}
    else:
      return None  # No solution exists
  
    
class ImprovedBacktrackingColorer(Colorer):
  def __init__(self, G: nx.Graph, n_colors: int):
    self.n_color = n_colors
    self.G = G.copy()
    
  def forward_checking(self, node: int, color: int) -> None:
    for neighbor in self.G.neighbors(node):
      if self.G.nodes[neighbor]['color'] is None:
        self.G.nodes[neighbor]['legal_colors'].discard(color)
  
  def restore_legal_colors(self, node: int, color: int) -> None:
    for neighbor in self.G.neighbors(node):
      if self.G.nodes[neighbor]['color'] is None:
        self.G.nodes[neighbor]['legal_colors'].add(color)
        
  def minimum_remaining_values_node(self) -> int:
    min_node = None
    min_legal_colors = float('inf')
    for node in self.G.nodes:
      if self.G.nodes[node]['color'] is None:
        # Tiebreaker: choose the node involved in more constraints
        if len(self.G.nodes[node]['legal_colors']) == min_legal_colors:
          if self.G.degree[node] > self.G.degree[min_node]:
            min_node = node
        elif len(self.G.nodes[node]['legal_colors']) < min_legal_colors:
          min_node = node
          min_legal_colors = len(self.G.nodes[node]['legal_colors'])
    return min_node
  
  def least_constraining_value(self, node: int) -> list[int]:
    legal_colors = self.G.nodes[node]['legal_colors']
    count = {}
    for color in legal_colors:
      count[color] = 0
      for neighbor in self.G.neighbors(node):
        if self.G.nodes[neighbor]['color'] is None and color in self.G.nodes[neighbor]['legal_colors']:
          count[color] += 1
    return sorted(legal_colors, key=lambda x: count[x])
  
  def color_node(self, node):
    next_node = self.minimum_remaining_values_node()
    
    if next_node is None:
      return True  # All nodes are colored
    
    if len(self.G.nodes[node]['legal_colors']) == 0:
      return False
    
    for color in self.least_constraining_value(node):
      self.G.nodes[node]['color'] = color
      self.forward_checking(node, color)
      if self.color_node(next_node):
        return True
      self.G.nodes[node]['color'] = None
      self.restore_legal_colors(node, color)
    
    return False  # No valid coloring found
  
  def color(self) -> dict[int, int] | None:
    sys.setrecursionlimit(10000)
    try:
      first_node = next(iter(self.G.nodes))
    except StopIteration:
      return {}
    for node in self.G.nodes:
      self.G.nodes[node]['color'] = None
      self.G.nodes[node]['legal_colors'] = set(range(self.n_color))
    if self.color_node(first_node):
      return {node: self.G.nodes[node]['color'] for node in self.G.nodes}
    else:
      return None  # No solution exists
    
    

class AC3BacktrackingColorer(Colorer):
  def __init__(self, G: nx.Graph, n_colors: int):
    self.n_color = n_colors
    self.G = G.copy()
    
  def forward_checking(self, node: int, color: int) -> None:
    for neighbor in self.G.neighbors(node):
      if self.G.nodes[neighbor]['color'] is None:
        self.G.nodes[neighbor]['legal_colors'].discard(color)
        
  def restore_legal_colors(self, node: int, color: int) -> None:
    for neighbor in self.G.neighbors(node):
      if self.G.nodes[neighbor]['color'] is None:
        self.G.nodes[neighbor]['legal_colors'].add(color)
        
  def minimum_remaining_values_node(self) -> int:
    min_node = None
    min_legal_colors = float('inf')
    for node in self.G.nodes:
      if self.G.nodes[node]['color'] is None:
        # Tiebreaker: choose the node involved in more constraints
        if len(self.G.nodes[node]['legal_colors']) == min_legal_colors:
          if self.G.degree[node] > self.G.degree[min_node]:
            min_node = node
        elif len(self.G.nodes[node]['legal_colors']) < min_legal_colors:
          min_node = node
          min_legal_colors = len(self.G.nodes[node]['legal_colors'])
    return min_node
    
  def least_constraining_value(self, node: int) -> list[int]:
    legal_colors = self.G.nodes[node]['legal_colors']
    count = {}
    for color in legal_colors:
      count[color] = 0
      for neighbor in self.G.neighbors(node):
        if self.G.nodes[neighbor]['color'] is None and color in self.G.nodes[neighbor]['legal_colors']:
          count[color] += 1
    return sorted(legal_colors, key=lambda x: count[x])
  
  def ac3(self) -> bool:
    queue = [(i, j) for i, j in self.G.edges]
    while queue:
      i, j = queue.pop(0)
      if self.revise(i, j):
        if len(self.G.nodes[i]['legal_colors']) == 0:
          return False
        for k in self.G.neighbors(i):
          queue.append((k, i))
    return True
  
  def revise(self, i: int, j: int) -> bool:
    revised = False
    for color in self.G.nodes[i]['legal_colors']:
      if not any((j_color != color) for j_color in self.G.nodes[j]['legal_colors']):
        self.G.nodes[i]['legal_colors'].discard(color)
        revised = True
    return revised
  
  def color_node(self, node):
    sys.setrecursionlimit(10000)
    
    next_node = self.minimum_remaining_values_node()
    
    if next_node is None:
      return True  # All nodes are colored
    
    if len(self.G.nodes[node]['legal_colors']) == 0:
      return False
    
    for color in self.least_constraining_value(node):
      self.G.nodes[node]['color'] = color
      self.forward_checking(node, color)
      if self.color_node(next_node):
        return True
      self.G.nodes[node]['color'] = None
      self.restore_legal_colors(node, color)
    
    return False  # No valid coloring found
  
  def color(self) -> dict[int, int] | None:
    try:
      first_node = next(iter(self.G.nodes))
    except StopIteration:
      return {}
    for node in self.G.nodes:
      self.G.nodes[node]['color'] = None
      self.G.nodes[node]['legal_colors'] = set(range(self.n_color))
    if self.ac3():
      if self.color_node(first_node):
        return {node: self.G.nodes[node]['color'] for node in self.G.nodes}
    return None
  
  
  