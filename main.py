import sys
import pathlib
import networkx as nx
import matplotlib.pyplot as plt
from Colorer import BuildInColorer, check_coloring, NaiveBacktrackingColorer, Colorer, ImprovedBacktrackingColorer, AC3BacktrackingColorer
import timeit
import multiprocessing
from multiprocessing.connection import Connection, Pipe

COLORS = [
  '#ff0000',  # red
  '#00ff00',  # green
  '#0000ff',  # blue
  '#ffff00',  # yellow
  '#ff00ff',  # magenta
  '#00ffff',  # cyan
  '#ff8000',  # orange
  '#8000ff',  # purple
  '#0080ff',  # light blue
  '#ff0080',  # pink
  '#80ff00',  # light green
  '#0080ff',  # light blue
  '#f3f3f3',  # light grey
  '#3f3f3f',  # dark grey
]


def read_input(input_filename: pathlib.Path) -> tuple[int, list[tuple[int, int]]]:
  n_colors = None
  edges = []
  
  with open(input_filename, 'r') as file:
    for line in file:
      if line[0] == '#':
        continue
      if n_colors is None:
        line = line.lower().strip().split('=')
        if len(line) != 2:
          raise Exception("Color count should be defined in the first line: 'colors = <number>'")
        if line[0].strip() != 'colors':
          raise Exception("Color count should be defined in the first line: 'colors = <number>'")
        try:
          n_colors = int(line[1].strip())
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
  
  if n_colors is None:
    raise Exception("Color count should be defined in the first line: 'colors = <number>'")
  
  return n_colors, edges


def parse_args(argv) -> pathlib.Path:
  if len(argv) != 2:
    raise Exception("Usage: main.py <input_filename>")
  input_filename = pathlib.Path(argv[1])
  if not input_filename.exists():
    raise Exception(f"File {input_filename} does not exist")
  if not input_filename.is_file():
    raise Exception(f"{input_filename} is not a file")
  return input_filename


def draw_colored_graph(graph: nx.Graph, colors: list[str]):
  # Kamada-Kawai produces repeatable results
  fig, ax = plt.subplots(figsize=(20, 20))
  pos = nx.kamada_kawai_layout(graph)
  nx.draw(graph, pos, with_labels=True, node_color=colors, edge_color='grey', ax=ax)
  plt.show()


def main(argv):
  input_filename = parse_args(argv)
  
  n_colors, edges = read_input(input_filename)
  
  graph = nx.Graph()
  graph.add_edges_from(edges)
  
  colorer = NaiveBacktrackingColorer(graph, n_colors)
  
  solution = colorer.color()
  
  if solution:
    if not check_coloring(graph, solution):
      print("Invalid coloring found", file=sys.stderr)
    print("# Node,Color")
    nodes = sorted(solution.keys())
    for node in nodes:
      print(f"{node}:{solution[node]}")
  else:
    print("No solution exists")

def runner(f_in: str, f_out: str, colorer_class: type[Colorer], conn: Connection = None):
  n_colors, edges = read_input(pathlib.Path(f_in))
  
  graph = nx.Graph()
  graph.add_edges_from(edges)
  
  colorer = colorer_class(graph, n_colors)
  
  start = timeit.default_timer()
  solution = colorer.color()
  stop = timeit.default_timer()
  
  if solution:
    if not check_coloring(graph, solution):
      print(f"Invalid coloring found for {f_in}", file=sys.stderr)
    with open(f_out, 'w') as file:
      nodes = sorted(solution.keys())
      for node in nodes:
        file.write(f"{node}:{solution[node]}\n")
  else:
    print(f"No solution exists for {f_in}")
  if conn:
    conn.send(stop - start)
    conn.close()
  return stop - start

  
def test(time_limit: int):
  for i in range(1, 12):
    parent_conn, child_conn = Pipe()
    proc = multiprocessing.Process(target=runner, args=(f"input-{i}.txt", f"output-{i}.txt", AC3BacktrackingColorer, child_conn))
    proc.start()
    proc.join(timeout=time_limit)
    if proc.is_alive():
      proc.terminate()
      print(f"Test {i} failed: time limit exceeded")
    else:
      color_time = parent_conn.recv()
      print(f"Test {i} passed: {color_time} seconds")
      
    

      

if __name__ == "__main__":
  main(sys.argv)
  # test(20)
