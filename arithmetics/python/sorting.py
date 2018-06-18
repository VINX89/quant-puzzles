#!/usr/bin/env python
from math import floor
from random import randint

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
    n_left = int(floor(n))
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

def get_median(a,a_idx,b,b_idx,c,c_idx):
    """Get median of three numbers
    @param {a,b,c} {first,second,third} number
    @param {a_idx,b_idx,c_idx} position of {first,second,third} number in the array
    @return the index of the number corresponding to the median
    """

    if a<=b:
        if c<=a:
            return a_idx
        elif c>=a and c<=b:
            return c_idx
        else:
            return b_idx
    else:
        if c<=b:
            return b_idx
        elif c>=b and c<=a:
            return c_idx
        else:
            return a_idx
            

def select_pivot(x, left, right, strategy=1):
    """Choose a 'pivot' for the partition
    routine implemented by the QuickSort algorithm.
    
    @param x input array (list)
    @param left starting position of the sequence to be partitioned
    @param right ending position of the sequence to be partitioned
    @param strategy code that identifies the strategy to choose the pivot:
           1 -> take a random pivot (default)
           2 -> take the first element on the left
           3 -> take the last element on the right
           4 -> take the median between first, middle and right elements
           for all the strategies other than 2, the chosen pivot is 
           swapped with the first element on the left as preprocessing step
    @return pivot and its (final) position
    """

    if strategy==1:
        idx = randint(left, right)
        x[left], x[idx] = x[idx], x[left]
        return x[left], left
    elif strategy==2:
        return x[left], left
    elif strategy==3:
        x[left], x[right] = x[right], x[left]
        return x[left], left
    elif strategy==4:
        low = x[left]
        hi = x[right]
        mid_idx = left + int(floor(right-left)/2)
        mid = x[mid_idx]
        median_idx = get_median(low,left,mid,mid_idx,hi,right)
        x[left], x[median_idx] = x[median_idx], x[left]
        return x[left], left
    else:
        raise ValueError("The strategy code must be in [1,4]")

def partition(x, left, right, strategy=1):
    """Partition a sequence according to a given pivot.
    @param x input array (list)
    @param left starting position of the sequence to be partitioned
    @param right ending position of the sequence to be partitioned
    @param strategy see select_pivot for the details
    @return (final) position of the pivot after the partition
    """

    pivot, p = select_pivot(x, left=left, right=right, strategy=strategy) 
    i = p+1
    
    for j in range(p+1, right+1):
        if x[j] < pivot:
            x[j], x[i] = x[i], x[j]
            i += 1
    x[left], x[i-1] = x[i-1], x[left]

    return i-1 

def quick_sort(x, n_comp, left=None, right=None, strategy=1):
    """Implement the QuickSort algorithm to sort array,
    having an average speed of O(n*logn).
    The sorting in made in-place (no copies of the input array are produced)
    @param x input array to sort (list)
    @param n_comp counter that keeps track of the number of 'comparisons'
           between the 'pivot' and the other elements during
           the 'partitioning' of the array. It has to be a 
           size-one list initialised to zero (e.g. n_comp = [0]) in order to be passed
           by reference (the C++ equivalent would be int n_comp; &n_comp)
    @param left starting position of the sequence to be partitioned (default=None, take first element)
    @param right ending position of the sequence to be partitioned (default=None, take last element)
    @strategy see select_pivot function for more details
    """

    if left==None and right==None:
        n=len(x)
        l=0
        r=n-1
    else:
        l=left
        r=right
        n=r-l+1

    if n<2:
        return
    
    p = partition(x, left=l, right=r, strategy=strategy)
    n_comp[0] += r-l

    quick_sort(x, n_comp, left=l, right=p-1, strategy=strategy)
    quick_sort(x, n_comp, left=p+1, right=r, strategy=strategy)
