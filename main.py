import sys
import pathlib
import networkx as nx
import matplotlib.pyplot as plt

COLORS = [
  '#ff0000', # red
  '#00ff00', # green
  '#0000ff', # blue
  '#ffff00', # yellow
  '#ff00ff', # magenta
  '#00ffff', # cyan
  '#ff8000', # orange
  '#8000ff', # purple
  '#0080ff', # light blue
  '#ff0080', # pink
  '#80ff00', # light green
  '#0080ff', # light blue
  '#f3f3f3', # light grey
  '#3f3f3f', # dark grey
]

def read_input(input_filename: pathlib.Path) -> tuple[int, list[tuple[int, int]]]:
  colors = None
  edges = []
  
  with open(input_filename, 'r') as file:
    for line in file:
      if line[0] == '#':
        continue
      if colors is None:
        line = line.lower().strip().split('=')
        if len(line) != 2:
          raise Exception("Color count should be defined in the first line: 'colors = <number>'")
        if line[0].strip() != 'colors':
          raise Exception("Color count should be defined in the first line: 'colors = <number>'")
        try:
          colors = int(line[1].strip())
        except ValueError:
          raise Exception("Color count should be defined in the first line: 'colors = <number>'")
        continue
      line = line.strip().split(',')
      if len(line) != 2:
        raise Exception("Each line should contain two numbers separated by a comma.")
      try:
        edges.append((int(line[0]), int(line[1])))
      except ValueError:
        raise Exception("Each line should contain two numbers separated by a comma.")
  
  if colors is None:
    raise Exception("Color count should be defined in the first line: 'colors = <number>'")
  
  return colors, edges

def parse_args(argv) -> pathlib.Path:
  if len(argv) != 2:
    raise Exception("Usage: main.py <input_filename>")
  input_filename = pathlib.Path(argv[1])
  if not input_filename.exists():
    raise Exception(f"File {input_filename} does not exist")
  if not input_filename.is_file():
    raise Exception(f"{input_filename} is not a file")
  return input_filename

def color_graph(colors: int, edges: list[tuple[int, int]]) -> list[int]:
  graph = nx.Graph()
  graph.add_edges_from(edges)
  
  return nx.coloring.equitable_color(graph, num_colors=colors)

def draw_colored_graph(graph: nx.Graph, colors: list[str]):
  # Kamada-Kawai produces repeatable results
  fig, ax = plt.subplots(figsize=(20, 20))
  pos = nx.kamada_kawai_layout(graph)
  nx.draw(graph, pos, with_labels=True, node_color=colors, edge_color='grey', ax=ax)
  plt.show()
  
  
def main(argv):
  input_filename = parse_args(argv)
  
  colors, edges = read_input(input_filename)
  
  graph = nx.Graph()
  graph.add_edges_from(edges)
  max_degree = max([graph.degree[node] for node in graph.nodes])
  print(f"Max degree: {max_degree}")
  
  # colors = color_graph(colors, edges)
  # colormap =[
  #   COLORS[colors[node]] for node in graph.nodes
  # ]
  #
  # draw_colored_graph(graph, colormap)
  
  
      


if __name__ == "__main__":
  main(sys.argv)
