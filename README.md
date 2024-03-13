# Project 2 CSP
Author: Abbas Aliyev

[Link to the project](https://github.com/Capta1n-n9m0/GWU-AI-Proj2-Coloring)

## Introduction
In this project, we are going to solve a constraint satisfaction problem (CSP) using the backtracking algorithm. I am going to implement Minimum Remaining Values (MRV) and Least Constraining Value (LCV) heuristics to improve the performance of the backtracking algorithm. On top of that I will implement forward checking and arc consistency to further improve the performance of the backtracking algorithm.

## Problem
The problem is to assign a color to each region in a map such that no two adjacent regions have the same color. The map is represented as a graph, where each region is a node and each edge represents an adjacency relationship between two regions. The graph is given as an adjacency list. The colors are represented as integers. The goal is to find a valid coloring of the map, if one exists.

## Implementation
The project is implemented in Python. The main file is `main.py`, which contains the main function that reads the input file, constructs the graph, and calls the backtracking algorithm to solve the CSP. For the graph representation I am using `networkx` library. Coloring algorithm is implemented in `Coloring.py` file. The file contains the implementation of the backtracking algorithm, as well as the heuristics and consistency checks. The input file is given as a command line argument to the main function. The input file is a text file that contains the graph in the following format:
```
#Any comments must start with a hash symbol
#The first line contains the number of colors
colors = 3
#The rest of the file contains the graph as an edge list
#Each line contains two integers, which represent the indices of the two nodes that are connected by an edge
0 1
0 2
1 2
```
The output of the program is the coloring of the graph, if one exists. The output is printed to the console in the following format:
```
0:1
1:2
2:0
```     
Each line contains a node index and the color assigned to that node. The output is printed in the order of the node indices.

## Usage
To run the program, you need to have Python installed on your machine. You can run the program by executing the following command in the terminal:
``` 
python main.py input.txt
```
Where `input.txt` is the input file that contains the graph. The output will be printed to the console.

For the testing purposes, I have included a few input files. You can use these files to test the program.

## Conclusion
In this project, I have implemented a backtracking algorithm to solve a constraint satisfaction problem. I have also implemented heuristics and consistency checks to improve the performance of the backtracking algorithm. The program is able to solve the graph coloring problem for small graphs. However, the performance of the program may degrade for larger graphs. Interestingly, I have noticed that the largest improvement by of the speed of the algorithm is happened when I implemented forward checking functionality. Everything else didn't provide significant improvements or even slowed down the execution. In the future, I would like to improve the performance of the program by implementing more advanced heuristics and consistency checks. I would also like to implement the program in a more efficient language, such as C++.

