#!/usr/bin/env python
import numpy as np
from math import sqrt

def get_binomial_prob(passed, trials, verbose=True):
    """Compute the binomial probability of success

    @param passed boolean array indicating if the given trial is 
           successful (True) or not (False)
    @param trials number of trials
    @param verbose print probability and uncertainty
    @return values prob, prob_err (probability and its uncertainty
    """
    success = float( np.sum( map(int, passed) ) )
    prob = success / float(trials)
    prob_err = (1./float(trials)) * sqrt(success*(1.-success/float(trials)))
    if verbose:
        print "Probability:"
        print "%lf +/- %lf" % (prob, prob_err)
    return prob, prob_err
