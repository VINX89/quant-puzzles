#!/usr/bin/env python
import os, sys

sys.path.append("../python")
from sorting import quick_sort

if __name__ == "__main__":

    dummy1 = [4,2,5,3,1]
    n_comp1 = [0]
    print "Dummy check 1: sort"
    print dummy1
    print "using always first 'pivot' on the left"
    quick_sort(dummy1, n_comp1, strategy=2)
    print dummy1
    print "(number of comparisons = %d)" % n_comp1[0]

    dummy2 = [4,2,5,3,1]
    n_comp2 = [0]
    print "Dummy check 2: sort"
    print dummy2
    print "using always last 'pivot' on the right"
    quick_sort(dummy2, n_comp2, strategy=3)
    print dummy2
    print "(number of comparisons = %d)" % n_comp2[0]
    
    dummy3 = [4,2,5,3,1]
    n_comp3 = [0]
    print "Dummy check 3: sort"
    print dummy3
    print "using always a random pivot"
    quick_sort(dummy3, n_comp3, strategy=1)
    print dummy3
    print "(number of comparisons = %d)" % n_comp3[0]
