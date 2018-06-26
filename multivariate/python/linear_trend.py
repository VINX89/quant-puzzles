#!/usr/bin/env python
import os, sys
import numpy as np
import math
import statsmodels.api as sm

class LinearTrend(object):
    """
    """
    def __init__(self, beta, varepsilon, covx, mux, check_consistency=True):
        beta = np.array(beta)
        covx = np.array(covx)
        mux = np.array(mux)
        if check_consistency:
            self.check_consistency(beta, covx, mux)
        self.beta = beta
        self.varepsilon = varepsilon
        self.covx = covx
        self.mux = mux
        self.x = np.array([])
        self.y = np.array([])
    def check_consistency(self, beta, covx, mux):
        if np.shape(covx)[0] != np.shape(covx)[1]:
            raise ValueError("The input covariance matrix must be square")
        if len(beta) != np.shape(covx)[0]:
            raise ValueError("The dimensions of beta and covariance matrix must match")
        if len(mux) != np.shape(covx)[0]:
            raise ValueError("The dimensions of mux and covariance matrix must match")
        if not np.allclose(covx, covx.T):
            raise ValueError("The input covariance matrix must be symmetric")
        if not np.all( np.linalg.eigvals(covx)>0 ):
            raise ValueError("The covariance matrix must be positive definite")
    def set_x(self, x):
        self.x = x
    def generate_x(self, nsamples):
        self.x = np.random.multivariate_normal(mean=self.mux, cov=self.covx, size=nsamples)
    def generate_y(self, nsamples):
        self.generate_x(nsamples)
        epsilon = np.random.normal(loc=0.0, scale=math.sqrt(self.varepsilon), size=nsamples)
        betax = []
        for xi in self.x:
            betax.append( self.beta.dot(xi) )
        betax = np.array( betax )
        self.y =  betax + epsilon
    def estimate_beta_simple(self, x=None, y=None, verbose=True):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        lm = sm.OLS(y, x)
        lm_res = lm.fit()
        if verbose:
            print lm_res.summary()
        return lm_res.params, lm_res.bse
    def estimate_beta_bootstrap(self, nsamples=1000, verbose=True):
        idx = np.random.choice( len(self.x), len(self.x) )
        beta_mean = []
        beta_sigma = []
        for n in range(nsamples):
            if verbose:
                if n%100 == 0:
                    print "...bootstrapping sample %d" % n
            idx = np.random.choice( len(self.x), len(self.x) )
            x_boot = []
            y_boot = []
            for i in idx:
                x_boot.append( self.x[i] )
                y_boot.append( self.y[i] )
            mu, sigma = self.estimate_beta_simple(x_boot, y_boot, verbose=False)
            beta_mean.append( mu )
            beta_sigma.append( sigma )
        return np.mean(beta_mean, 0), np.std(beta_sigma, 0)
