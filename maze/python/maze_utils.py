#!/usr/bin/env python
import heapq
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import copy

class MazeCell(object):
    def __init__(self, x, y, iswall):
        """Initialize new maze cell.
        @param iswall wheter a cell is a wall (not-reachable) or not (empty)
        @param x coordinate
        @param y coordinate
        @param parent parent cell
        @param g cost to move from the starting cell to this cell (i.e. number of traversed cells)
        @param h estimation of the cost to move from this cell
                 to the ending cell (given by heuristic formula)
        @param f f = g + h
        """
        self.iswall = iswall
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        
    def print_cell(self):
        wall = "yes" if self.iswall else "no"
        if self.parent:
            print "Coordinates: (%d,%d), parent: (%d,%d), wall: %s, f=%d, g=%d, h=%d" % (self.x, 
                                                                                         self.y, 
                                                                                         self.parent.x, 
                                                                                         self.parent.y, 
                                                                                         wall, 
                                                                                         self.f, 
                                                                                         self.g, 
                                                                                         self.h)
        else:
            print "Coordinates: (%d,%d), no parent, wall: %s, f=%d, g=%d, h=%d" % (self.x, 
                                                                                   self.y, 
                                                                                   wall, 
                                                                                   self.f, 
                                                                                   self.g, 
                                                                                   self.h)

class Maze(object):
    """
    Implements "A*" algorithm for solving a N*M maze
    """
    def __init__(self, maze, start=None, end=None):
        """Prepare grid cells, walls.
        @param maze nested N*M list describing the maze
               empty cells identified as 0
               walls identified as 1
               e.g. 4*3 maze: [[0,1,0], [0,0,0], [1,1,0], [0,1,0]]
               By default, start = upper left and stop = bottom right
               unless specified differently with start and stop arguments.
        @param start grid starting point x,y tuple.
        @param end grid ending point x,y tuple.
        """
        self.maze = maze
        self.path = None
        # check maze (shape and consistency)
        if len(np.shape(maze)) != 2:
            raise ValueError("The input maze has to be 2-dimensional")
        self.grid_height = np.shape(maze)[0]
        self.grid_width = np.shape(maze)[1]
        # open list
        self.opened = []
        heapq.heapify(self.opened)
        # grid cells
        self.cells = []
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if maze[y][x]<0 or maze[y][x]>1:
                    raise ValueError("Only 0's and 1's are allowed in the maze")
                iswall = True if maze[y][x]==1 else False
                self.cells.append(MazeCell(x, y, iswall))
        # visited cells list
        self.closed = set()
        # endpoints
        if start is not None:
            if maze[start[1]][start[0]] == 1:
                raise ValueError("You can't assign the start to a cell with a wall")
            else:
                self.start = self.get_cell(*start)
        else:
            if maze[0][0] == 1:
                raise ValueError("A wall and the start (top left) are overlapping")
            else:
                self.start = self.get_cell(0,0)
        if end is not None:
            if maze[end[1]][end[0]] == 1:
                raise ValueError("You can't assign the stop to a cell with a wall")
            else:
                self.end = self.get_cell(*end)
        else:
            if maze[self.grid_height-1][self.grid_width-1] == 1:
                raise ValueError("A wall and the stop (bottom right) are overlapping")
            else:
                self.end = self.get_cell(self.grid_width-1, self.grid_height-1)

    def get_cost(self, cell):
        """Compute the (heuristic) cost h to move from this cell
        to the end of the maze
        @returns heuristic value h
        """
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def get_cell(self, x, y):
        """Returns a cell from the cells list.
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """        
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """Returns adjacent cells to a cell.
        Clockwise starting from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))
        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        """Update adjacent cell.
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 1
        adj.h = self.get_cost(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def plot_maze(self, output='maze.pdf'):
        """Plot maze
        @param output output file name
        Legend:
        -white: empty cells
        -black: walls
        -green: path (if defined)
        """
        cmap = ListedColormap(['w', 'k'])
        mazeplot = copy.deepcopy(self.maze)
        if self.path:
            cmap = ListedColormap(['w', 'k', 'g'])
            #Add path
            for p in self.path:
                mazeplot[p[1]][p[0]] = 2
        #Make plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        _ = ax.matshow(mazeplot,cmap=cmap)
        #Add start/end
        ax.text(self.start.x, self.start.y, "START", color='black', ha='center', va='center')
        ax.text(self.end.x, self.end.y, "END", color='black', ha='center', va='center')
        fig.savefig(output)

    def solve(self):
        """Solve maze, find path to ending cell.
        @returns path (or None if not found) and its lenght
        """
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, return found path
            if cell is self.end:
                self.path = self.get_path()
                pathlen = np.shape(self.path)[0]
                return self.path, pathlen
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if not adj_cell.iswall and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 1:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))
            if len(self.opened)==0:
                print "Warning: impossible maze!"
                return None, 0
