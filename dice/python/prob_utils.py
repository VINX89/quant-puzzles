#!/usr/bin/env python
import numpy as np
from math import sqrt

def get_binomial_prob(passed, trials, verbose=True):
    """Compute the binomial probability of success

    @param passed boolean array indicating if the given trial is 
           successful (True) or not (False)
    @param trials number of trials
    @param verbose print probability and uncertainty
    @return values prob, prob_err (probability and its uncertainty)
    """
    success = float( np.sum( map(int, passed) ) )
    prob = success / float(trials)
    prob_err = (1./float(trials)) * sqrt(success*(1.-success/float(trials)))
    if verbose:
        print "Probability:"
        print "%lf +/- %lf" % (prob, prob_err)
    return prob, prob_err

def check_subset(arr, target):
    """
    """    
    #print "arr"
    #print arr
    sorted = np.sort( arr )
    #print "sorted"
    #print sorted
    filt = []
    for a in sorted:
        filt.append( filter(lambda x: x <= target, a) )
    filt = np.array( filt )
    #print "filt"
    #print filt

    passed = np.zeros( len(filt) )
    for n, f in enumerate(filt):
        for i, el in enumerate(f):
            if el==target:
                passed[n] = 1
                break
            else:
                test = el
                for j in range(i+1, len(f)):
                    test += f[j]  
                    if test == target:
                        passed[n] = 1
                        break
    passed = np.array( passed, dtype=bool )
    #print "passed"
    #print passed
    return passed
