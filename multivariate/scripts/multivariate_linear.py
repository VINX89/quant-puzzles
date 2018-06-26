import os, sys
import numpy as np
sys.path.append("../python")

from linear_trend import LinearTrend

if __name__ == "__main__":

    beta = [1, 0.5, 0]
    varepsilon = 0.1
    covx = [ [1.0, 0.1, 0.999], [0.1, 1.0, 0.1], [0.999, 0.1, 1.0] ]
    mux = [0.0, 0.0, 0.0]

    lt = LinearTrend(beta, varepsilon, covx, mux)
    lt.generate_y(100)
    x = lt.x
    y = lt.y
    mean_beta_simple, sigma_beta_simple = lt.estimate_beta_simple()
    print mean_beta_simple
    print sigma_beta_simple
    
    mean_beta_boot, sigma_beta_boot = lt.estimate_beta_bootstrap()
    print mean_beta_boot
    print sigma_beta_boot
