#!/usr/bin/env python                                                                                                                          
import os, sys

sys.path.append("../python")
from sorting import count_inversions, merge_sort

if __name__ == "__main__":

    dummy1 = range(5)
    print "Dummy check 1: count inversions in"
    print dummy1
    print "Inversions: "+str( count_inversions(dummy1) )

    dummy2 = dummy1[::-1]
    print "Dummy check 2: count inversions in"
    print dummy2
    print "Inversions: "+str( count_inversions(dummy2) )

    dummy3 = [4,2,6,5,7,3]
    print "Dummy check 3: count inversions in"
    print dummy3
    print "Inversions: "+str( count_inversions(dummy3) )

    data = []
    with open("../data/IntegerArray.txt","r") as file:
        for line in file:
            data.append( int( line.replace("\n","") ) ) 
    print "Count inversions in array from file IntegerArray.txt"
    print "Inversions: "+str( count_inversions(data) )
