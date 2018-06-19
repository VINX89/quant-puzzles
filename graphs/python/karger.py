#!/usr/bin/env python
from math import log
from random import randint
import copy
import numpy as np
import matplotlib.pyplot as plt

class Vertex(object):
    """Class representing a vertex
    and its edges (i.e. list of connected vertices) in a graph.
    
    To instantiate a vertex:
    vertex = Vertex(v=v, e=e)
    
    v is the list of vertices. 
    If it contains a single number, then a single
    vertex is represented.
    If it contains multiple values, this means that 
    the vertex is built as a 'supervertex', originating
    from the contraction of different vertices.

    e is the list of edges, i.e. the other vertices
    that are connected to this one (or to the list
    or vertices grouped to build this one).
    """
    def __init__(self, v=None, e=None):
        self.v = [] if v is None else v
        self.e = [] if e is None else e
    def add_vertices(self, v):
        self.v += v
    def add_edges(self, e):
        self.e += e
    def contract(self, vertex):
        if set(self.e).isdisjoint(vertex.v):
            raise ValueError("Trying to contract non-connected vertices")
        #Group contracting vertices together
        self.v += vertex.v
        #Group all edges, then remove ones that appear in vertices list to:
        #1)remove self loops
        #2)remove contracted edge
        self.e += vertex.e
        self.e = list(filter(lambda x: x not in self.v, self.e))
    def print_vertex(self):
        print "List of vertices:"
        print self.v
        print "List of edges:"
        print self.e

class Graph(object):
    """Class representing a non-oriented graph.
    
    To instantiate a graph:
    graph = Graph(adjlist=adjlist)

    adjlist is the 'adjacency list' representing
    the graph: it contains multiple lists (one for
    each vertex), where the first element is the vertex
    index, while the other elements (from 2nd to last)
    are the edges (other vertices connected to this one).

    Example:

    1   4
     \ / \
      3 - 5 
     /
    2

    [ [1,3], [2,3], [3,1,2,4,5], [4,3,5], [5,3,4] ]
    """
    def __init__(self, adjlist=None):
        self.adjlist = []
        if adjlist is not None:
            self.add_vertices(adjlist)
        self.min_cuts = []
    def clone(self):
        return copy.deepcopy(self)
    def add_vertices(self, adjlist):
        for vertex in adjlist:
            self.adjlist.append( Vertex(v=[vertex[0]], e=vertex[1:]) )
    def get_random_edge(self):
        vertex1 = self.adjlist[ randint(0, len(self.adjlist)-1 ) ]
        vtx1 = self.adjlist.index( vertex1 )
        rdm2 = randint(0, len(vertex1.e))
        vertex2 = vertex1.e[ randint(0, len(vertex1.e)-1) ]
        for vtx2, vtx in enumerate(self.adjlist):
            if vertex2 in vtx.v:
                return vtx1, vtx2
    def contract_vertices(self, vtx1, vtx2):
        self.adjlist[vtx1].contract( self.adjlist[vtx2] )
        self.adjlist.pop( vtx2 )
    def find_min_cut(self, ncalls=-1, debug=False):
        """Find the minimum number of cuts using the Karger algorithm.
        @param ncalls number of iterations. The probability P that
                      the minimum number of cuts is NOT found
                      after ncalls iterations is:
                      P <= (1 - 1/nvtx^2 )^ncalls
                      The defauls is ncalls = nvtx*log(nvtx),
                      so that P<=1/nvtx^2
                      (this is a quite time-consuming requirement)
        @param debug print out some debug information
        @returns the minimum number of cuts, two possible partitions
                 realising that (as lists of vertex indices)
        """
        min_cut = len(self.adjlist)
        cutA = []
        cutB = []
        if ncalls < 0:
            #Take n^2*log(n) by default to have the probability
            #of finding at least one min cut as P = 1 - 1/n
            ncalls = int(len(self.adjlist)**2 * log( len(self.adjlist) ))
        if debug:
            print "[DEBUG] Graph.find_min_cut(...): number of iterations "+str(ncalls)
        for i in range(ncalls):
            if debug and i%50 == 0:
                print "[DEBUG] Graph.find_min_cut(...): ...iteration "+str(i)
            thisgraph = self.clone()
            while( len(thisgraph.adjlist)>2 ):
                #Get random pair of connected vertices
                vtx1, vtx2 = thisgraph.get_random_edge()
                #Contract them
                thisgraph.contract_vertices(vtx1, vtx2)
                #Return cut
                if len(thisgraph.adjlist)==2:
                    this_min = min( len(thisgraph.adjlist[0].e), len(thisgraph.adjlist[1].e) )
                    if this_min < min_cut:
                        min_cut = this_min
                        cutA = thisgraph.adjlist[0].v
                        cutB = thisgraph.adjlist[1].v
                    self.min_cuts.append( min_cut )
            del thisgraph
        return min_cut, cutA, cutB
    def plot_convergence(self, title):
        """Plot the minimum number of cuts
        as a function of the iteration step.
        It can be useful to optimise the number of
        iterations: if the curve reaches a plateau,
        then it is very likely that no more iterations
        are needed.
        @param title name of the output file
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(self.min_cuts)
        plt.xlabel('iteration')
        plt.ylabel('min cut found')
        fig.savefig(title)
