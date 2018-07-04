import os, sys
import numpy as np
import math
sys.path.append("../python")

from linear_trend import LinearTrend

if __name__ == "__main__":

    beta = np.array( [1, 0.5, 0] )
    varepsilon = 0.1
    covx = np.array( [ [1.0, 0.1, 0.999], [0.1, 1.0, 0.1], [0.999, 0.1, 1.0] ] )
    mux = np.array( [0.0, 0.0, 0.0] )

    lt = LinearTrend(beta)
    lt.generate_normal(100, mux, covx, varepsilon)
    lt_simple = lt.estimate_beta_ols()
    print "Single regressor:"
    print "Fitted betas"
    print lt_simple.params
    print "Variances"
    print np.array( [x**2 for x in lt_simple.bse] )
    print ""

    beta_bagging = lt.estimate_beta_bagging(nsamples=1000, verbose=False)
    print "Bootstrap aggregation (Bagging):"
    print "Average betas"
    print np.mean(beta_bagging, 0)
    print "...with the following number of beta=0 occurrences:"
    nonzeros = np.count_nonzero(beta_bagging, axis=0)
    print 1000-nonzeros[0], 1000-nonzeros[1], 1000-nonzeros[2]
    print "Average variances"
    print np.var(beta_bagging, 0)
    print ""

    print "Optimising lasso regularisation parameter..."
    bestl = lt.optimise_regularisation(lmin=0.0, lmax=0.5, nsteps=200, nfolds=5)
    print ""

    beta_bagging = lt.estimate_beta_bagging(nsamples=1000, l=bestl, verbose=False)
    print "Bootstrap aggregation (Bagging) with Lasso regularisation (optimal l):"
    print "Average betas"
    print np.mean(beta_bagging, 0)
    print "...with the following number of beta=0 occurrences:"
    nonzeros = np.count_nonzero(beta_bagging, axis=0)
    print 1000-nonzeros[0], 1000-nonzeros[1], 1000-nonzeros[2]
    print "Average variances"
    print np.var(beta_bagging, 0)
    print ""

    beta_bagging = lt.estimate_beta_bagging(nsamples=1000, l=0.1, verbose=False)
    print "Bootstrap aggregation (Bagging) with Lasso regularisation (l=0.1):"
    print "Average betas"
    print np.mean(beta_bagging, 0)
    print "...with the following number of beta=0 occurrences:"
    nonzeros = np.count_nonzero(beta_bagging, axis=0)
    print 1000-nonzeros[0], 1000-nonzeros[1], 1000-nonzeros[2]
    print "Average variances"
    print np.var(beta_bagging, 0)
    print ""
