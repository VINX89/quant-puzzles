#!/usr/bin/env python
import os, sys

sys.path.append("../python")
from karger import Graph

if __name__ == "__main__":

    dummy_list = [ [1,3], [2,3], [3,1,2,4,5], [4,3,5], [5,3,4] ]
    dummy_graph = Graph( adjlist = dummy_list )
    min_cut, cutA, cutB = dummy_graph.find_min_cut(debug=True)
    print "Dummy check on adjacent list:"
    print dummy_list
    print "Minimum cut: "+str(min_cut)
    print "First subgraph:"
    print cutA
    print "Second subgraph:"
    print cutB

    print ""
    print "Find minimum cut for graph defined in kargerMinCut.txt:"
    adjlist = []
    with open("../data/kargerMinCut.txt","r") as file:
        for line in file:
            adjlist.append( [int(x) for x in line.split() ] )
    graph = Graph( adjlist = adjlist )
    min_cut, cutA, cutB = graph.find_min_cut(ncalls=1000, debug=True)
    print "Minimum cut: "+str(min_cut)
    print "First subgraph:"
    print cutA
    print "Second subgraph:"
    print cutB
    graph.plot_convergence('convergence_min_cut.pdf')
