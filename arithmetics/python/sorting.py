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

def select_pivot(x, left, right, strategy=1):
    
    if strategy==1:
        idx = randint(left, right)
        x[left], x[idx] = x[idx], x[left]
        return x[left], left
    elif strategy==2:
        return x[left], left
    elif strategy==3:
        x[left], x[right] = x[right], x[left]
        return x[left], left
    else:
        raise ValueError("The strategy code must be in [1,3]")

def partition(x, left, right, strategy=1):
    
    pivot, p = select_pivot(x, left=left, right=right, strategy=strategy) 
    i = p+1
    
    for j in range(p+1, right+1):
        if x[j] < pivot:
            x[j], x[i] = x[i], x[j]
            i += 1
    x[left], x[i-1] = x[i-1], x[left]

    return i-1 

def quick_sort(x, n_comp, left=None, right=None, strategy=1):
    
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
    n_comp[0] += n_comp[0]+r-l-2 #r-p-1 - (p-1-l)

    quick_sort(x, n_comp, left=l, right=p-1, strategy=strategy)
    quick_sort(x, n_comp, left=p+1, right=r, strategy=strategy)
