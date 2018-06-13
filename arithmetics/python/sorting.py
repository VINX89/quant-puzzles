#!/usr/bin/env python
import math

def split(x, n):
    """Given an input array,
    it splits it into two parts,
    where the first part has length
    n and the second one
    contains the remaining elements

    @param x input array (as a list)
    @param n number of elements to put in the first subarray
    @returns the two subarrays (as lists)
    """
    n_left = int(math.floor(n))
    x_left = x[:n_left]
    x_right = x[n_left:]
    return x_left, x_right

def merge_sort(x):
    """Implements the 'merge sort'
    algorithm of speed O(n*logn)

    @param x the input array (as a list)
    @returns the sorted array (as a list) and the number of
    'inversions', i.e. when x[i]>x[j] when i<j
    """
    n = len(x)
    if n == 1:
        return x, 0

    x_left, x_right = split(x, n/2)

    x_left_sorted,_ = merge_sort(x_left)
    x_right_sorted,_ = merge_sort(x_right)

    i=0
    j=0
    x_sorted = []
    inv_split = 0
    n_left = len(x_left_sorted)
    n_right = len(x_right_sorted)
    do_left = True
    do_right = True
    for k in range( n_left+n_right ):
        if x_left_sorted[i]<x_right_sorted[j]:
            x_sorted.append( x_left_sorted[i] )
            i += 1
            if i==n_left:
                x_sorted += x_right_sorted[j:]
                break
        elif x_left_sorted[i]>=x_right_sorted[j]:
            x_sorted.append( x_right_sorted[j] )
            inv_split += len( x_left_sorted[i:] )
            j += 1
            if j==n_right:
                x_sorted += x_left_sorted[i:]
                break

    return x_sorted, inv_split

def count_inversions(x):
    """Implements a recursive algorithm 
    of speed O(n*logn) to count the number
    of 'inversions', i.e. when
    x[i]>x[j] with i<j.

    @param x input array (as a list)
    @returns number of inversions
    """
    n = len(x)
    if n == 1:
        return 0
    
    x_left, x_right = split(x, n/2)

    inv_left = count_inversions(x_left)
    inv_right = count_inversions(x_right)
    _, inv_split = merge_sort(x)
    
    return inv_left + inv_right + inv_split
    
