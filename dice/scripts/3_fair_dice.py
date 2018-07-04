#!/usr/bin/env python
import numpy as np
import math
import os, sys

sys.path.append("../python")
from prob_utils import get_binomial_prob, check_subset

def subset_prob(ndice, target, ntrials=1000000):
    
    outcome = np.random.randint(1, high=7, size=(ntrials, ndice))
    passed = check_subset(outcome, target)
    _,_ = get_binomial_prob(passed, ntrials)

if __name__ == "__main__":
    print "Probability of having a '3 subset' from 1 dice:"
    subset_prob(1, 3)
    print "Probability of having a '1 subset' (i.e. at least one 1) from 3 dice:"
    subset_prob(3, 1)
    print "Probability of having a '3 subset' from 3 dice:"
    subset_prob(3, 3)
    print "Probability of having a '4 subset' from 3 dice:"
    subset_prob(3, 4)
