#/use/bin/env python

import os, sys
sys.path.append("../python")

from maze_utils import Maze

normal = [[0, 0, 0, 0, 0, 1],
          [1, 1, 0, 0, 0, 1],
          [0, 0, 0, 1, 0, 0],
          [0, 1, 1, 0, 0, 1],
          [0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0, 0]]

impossible = [[0, 0, 0, 0, 0, 1],
              [1, 1, 0, 0, 0, 1],
              [0, 0, 0, 1, 0, 0],
              [0, 1, 1, 0, 0, 1],
              [0, 1, 0, 0, 1, 0],
              [0, 1, 0, 1, 0, 0],
              [0, 1, 0, 0, 1, 0] ]

def solve_maze(maze, start=None, end=None, output='maze.pdf'):    
    print "Input maze:"
    print maze
    the_maze = Maze(maze, start, end)
    path, pathlen = the_maze.solve()
    print "Path:"
    print path
    print "Lenght of path:"
    print pathlen
    the_maze.plot_maze(output)

if __name__ == "__main__":
    solve_maze(normal, output='normal.pdf')
    solve_maze(impossible, output='impossible.pdf')
