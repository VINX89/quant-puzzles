#!/usr/bin/env python
import os, sys, copy

sys.path.append("../python")
from sorting import quick_sort

if __name__ == "__main__":

    dummy1 = [3,2,4,1,5,8,6,9,7,0,12,11,10]
    n_comp1 = [0]
    print "Dummy check 1: sort"
    print dummy1
    print "using always first number on the left as pivot"
    quick_sort(dummy1, n_comp1, strategy=2)
    print dummy1
    print "(number of comparisons = %d)" % n_comp1[0]
    print ""

    dummy2 = [3,2,4,1,5,8,6,9,7,0,12,11,10]
    n_comp2 = [0]
    print "Dummy check 2: sort"
    print dummy2
    print "using always last number on the right as pivot"
    quick_sort(dummy2, n_comp2, strategy=3)
    print dummy2
    print "(number of comparisons = %d)" % n_comp2[0]
    print ""

    dummy3 = [3,2,4,1,5,8,6,9,7,0,12,11,10]
    n_comp3 = [0]
    print "Dummy check 3: sort"
    print dummy3
    print "using always a random pivot"
    quick_sort(dummy3, n_comp3, strategy=1)
    print dummy3
    print "(number of comparisons = %d)" % n_comp3[0]
    print ""

    dummy4 = [3,2,4,1,5,8,6,9,7,0,12,11,10]
    n_comp4 = [0]
    print "Dummy check 4: sort"
    print dummy4
    print "using always the median between first, middle and last in the array as pivot"
    quick_sort(dummy4, n_comp4, strategy=4)
    print dummy4
    print "(number of comparisons = %d)" % n_comp4[0]
    print ""

    data1 = []
    with open("../data/QuickSort.txt","r") as file:
        for line in file:
            data1.append( int( line.replace("\n","") ) )
    data2 = copy.deepcopy(data1)
    data3 = copy.deepcopy(data1)
    n_comp1 = [0]
    n_comp2 = [0]
    n_comp3 = [0]
    print "Get array from QuickSort.txt"
    print "Count comparison using first number as 'pivot'"
    quick_sort(data1, n_comp1, strategy=2)
    print "... number of comparisons %d" % n_comp1[0]
    print "Count comparison using last number as 'pivot'"
    quick_sort(data2, n_comp2, strategy=3)
    print "... number of comparisons %d" % n_comp2[0]
    print "Count comparison using median between first, middle and last numbers as 'pivot'"
    quick_sort(data3, n_comp3, strategy=4)
    print "... number of comparisons %d" % n_comp3[0]
