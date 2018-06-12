#!/usr/bin/env python
import math

def split(x, n):

    n_left = int(math.floor(n))
    x_left = x[:n_left]
    x_right = x[n_left:]
    return x_left, x_right

def merge_sort(x):
    
    n = len(x)
    if n == 1:
        return x, 0

    x_left, x_right = split(x, n)
    
    x_left_sorted = merge_sort(x_left)
    x_right_sorted = merge_sort(x_right)

    i=0
    j=0
    x_sorted = []
    inv_split = 0
    for k in range(n):
        if x_left_sorted[i]<x_right_sorted[j]:
            x_sorted.append( x_left_sorted[i] )
            i += 1
        else:
            x_sorted.append( x_right[j] )
            inv_split += len( x_left[i:] )
            j += 1
    
    return x_sorted, inv_split

def count_inversions(x):
    
    n = len(x)
    if n == 1:
        return x, 0
    
    x_left, x_right = split(x, n)

    inv_left = count_inversions(x_left)
    inv_right = count_inversions(x_right)
    _, inv_split = merge_sort(x)
    
    return inv_left + inv_right + inv_split
    
