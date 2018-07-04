#!/usr/bin/env python
import os, sys
import numpy as np
import math
import statsmodels.api as sm
import matplotlib.pyplot as plt

class LinearTrend(object):
    """Class implementing a simple multivariate regression
    model of the form:

    y = beta*x

    @param beta array of slope coefficients (numpy array)
    """
    def __init__(self, beta):
        self.beta = beta
        self.x = np.array([])
        self.y = np.array([])
    def check_consistency(self, beta, covx, mux):
        """Check whether the input given
        to generate a random sample from 
        normally-distributed x is consistent
        
        @param beta slope coefficients (numpy array)
        @param covx x covariance matrix (numpy array)
        @param mux array of mean values for each x (numpy array)
        """
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
    def evaluate(self, x=None, epsilon=None):
        """Evaluate y for a given dataset x
        
        @param x data sample (numpy array)
        @param epsilon a constant offset, e.g. random noise (numpy array)
        @returns the evaluated y (numpy array)
        """
        if x is None:
            x = self.x
        if epsilon is None:
            epsilon = np.zeros( len(x) )
        betax = []
        for xi in self.x:
            betax.append( self.beta.dot(xi) )
        betax = np.array( betax )
        y =  betax + epsilon
        return y
    def mse(self, x=None, y=None, beta=None):
        """Evaluate the average mean squared error

        @param x data sample (numpy array)
        @param y reference target (numpy array)
        @param beta slope coefficients (numpy array)
        @returns the average MSE
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if beta is None:
            beta = self.beta
        betax = []
        for xi in x:
            betax.append( beta.dot(xi) )
        betax = np.array( betax )
        return 1.0/len(y) * np.sum( pow(y - betax, 2) )
    def generate_normal(self, nsamples, mux, covx, varepsilon, check_consistency=True):
        """Generate a normally-distributed x-sample, and evaluate the corresponding y

        @param nsamples number of samples to generate
        @param mux array of mean values for each x (numpy array)
        @param covx x covariance matrix (numpy array)
        @param varepsilon variance of the random noise term
        @param check_consistency wheter the consistency of the input needs to be checked
        """
        if check_consistency:
            self.check_consistency(self.beta, covx, mux)
        self.x = np.random.multivariate_normal(mean=mux, cov=covx, size=nsamples)
        epsilon = np.random.normal(loc=0.0, scale=math.sqrt(varepsilon), size=nsamples)
        self.y = self.evaluate(epsilon=epsilon)
    def estimate_beta_ols(self, x=None, y=None, l=0.0, L1w=1.0, verbose=True):
        """Infer betas by means of an ordinary-least-squares (OLS) regression

        @param x data sample (numpy array)
        @param y target sample (numpy array)
        @param l regularisation coefficient term (0 for no regularisation)
        @param L1w weight given to the lasso regularisation (1 for pure lasso, 0 for pure ridge)
        @param verbose print some info
        @returns an instance of the fit results. See statsmodels.api documentation for more info
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        lm = sm.OLS(y, x)
        if l > 0:
            lm_res = lm.fit_regularized(alpha=l, L1_wt=L1w)
            if verbose:
                print "Regularized least-squares regression with l=%f, L1w=%f" % (l,L1w)
                print "Fitted parameters:"
                print lm_res.params
        else:
            lm_res = lm.fit()
            if verbose:
                print lm_res.summary()
        return lm_res
    def estimate_beta_bagging(self, nsamples=1000, l=0.0, L1w=1.0, verbose=True, plot=True):
        """Infer betas by means of repeated OLS on bootstrapped samples

        @param nsamples number of samples to bootstrap
        @param l regularisation coefficient term (0 for no regularisation)
        @param L1w weight given to the lasso regularisation (1 for pure lasso, 0 for pure ridge)
        @param verbose print some info
        @param plot whether to produce histograms showing the distribution of the estimated
               beta in each bootstrapping instance
        @returns array containing the betas evaluated at each step
        """
        beta_bagging = []
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
            mu = self.estimate_beta_ols(x_boot, y_boot, l=l, L1w=L1w, verbose=False).params
            beta_bagging.append( mu )
        beta_bagging = np.array( beta_bagging )
        if plot:
            for b in range(1,len(self.beta)+1):
                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.hist(beta_bagging[:,b-1])
                plt.xlabel(r'Estimated $\beta_{'+str(b)+'}$')
                plt.ylabel('Number of counts')
                fig.savefig('beta_%d_bagging_l%f.pdf' % (b,l))
        return beta_bagging
    def optimise_regularisation(self, lmin=0.0, lmax=0.2, nsteps=100, nfolds=5, L1w=1.0, verbose=False, plot=True, log=False):
        """Optimise the regularisation coefficient l by minimising the MSE
        For each value of l, a n-fold cross-validation is performed to evaluate the average MSE

        @param lmin minimum value of l to scan
        @param lmax maximum value of l to scan
        @param nsteps number of steps for the l scanning
        @param nfolds number of cross-validation folds
        @param L1w weight given to the lasso regularisation (1 for pure lasso, 0 for pure ridge)
        @param verbose print some info 
        @param plot whether to produce a plot showing the average MSE as a function of l
        @param log wheter to set a log scale for the x-axis of the MSE-l plot
        @returns the optimal l
        """
        if lmax<=lmin:
            raise ValueError("Must have lmin<lmax")
        step = (lmax-lmin) / float(nsteps)
        l = lmin
        idx = np.array( range(len(self.x)) )
        MSE = []
        MSEerr = []
        lam = []
        for s in range(nsteps):
            if verbose:
                print("Evaluating l=%f..." % l )
            np.random.shuffle(idx)
            while True:
                try:
                    idxs = np.split( idx, nfolds )
                except:
                    print "Warning: nfolds=%d gives unbalanced splits. Trying %d..." % (nfolds, nfolds+1)
                    nfolds += 1
                    continue
                else:
                    break
            thismse = []
            for f in range(nfolds):
                mask = np.zeros(len(self.x), dtype=bool)
                mask[idxs[f]] = True
                evalx = self.x[mask]
                evaly = self.y[mask]
                trainx = self.x[~mask]
                trainy = self.y[~mask]
                lm_res = self.estimate_beta_ols(x=trainx, y=trainy, l=l, L1w=L1w, verbose=False)
                thismse.append( self.mse(x=evalx, y=evaly, beta=np.array(lm_res.params) ) )
            MSE.append( np.mean(thismse) )
            MSEerr.append( np.std(thismse) )
            lam.append( l )
            l += step
            if verbose:
                print "...current MSE: %f" % MSE[s]
        bestl = lam[ MSE.index(min(MSE)) ]
        print "Best l parameter: %f" % bestl
        if plot:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plt.errorbar(lam, MSE, yerr=MSEerr)
            plt.xlabel(r'$\lambda$')
            plt.ylabel('Mean squared error')
            if log:
                ax.set_xscale("log")
            fig.savefig('MSE.pdf')
        return bestl
