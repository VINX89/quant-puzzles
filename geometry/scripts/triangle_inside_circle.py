#!/usr/bin/env python
import os, sys
import numpy as np
from numpy import random as rn
from math import sqrt, sin, cos, pi
import matplotlib.pyplot as plt
sys.path.append("../python")

def angle_to_chord(angle):
    return 2.*sin(angle/2.)

def midpoint_to_chord(midpoint):
    return 2.*sqrt(1. - midpoint**2)

def get_binomial_prob(passed, trials):
    success = float( np.sum( map(int, passed) ) ) 
    prob = success / float(trials)
    prob_err = (1./float(trials)) * sqrt(success*(1.-success/float(trials)))
    return prob, prob_err

def get_chord_from_int_points(rho1, theta1, rho2, theta2):
    
    #Get straight line passing through the random pair of points
    x1 = rho1 * np.cos(theta1)
    y1 = rho1 * np.sin(theta1)
    x2 = rho2 * np.cos(theta2)
    y2 = rho2 * np.sin(theta2)

    m = (y1-y2) / (x1-x2)
    q = y1 - m*x1

    #Solve following system:
    #  x**2 + y**2 = 1
    #  y = m*x + q
    #to find intercepts (xA, yA) and (xB, yB)
    #We find:
    #  xA = ( -m*q + sqrt( m**2 * q**2 - (q**2-1)*(1+m**2) ) ) / (1+m**2)
    #  xB = ( -m*q - sqrt( m**2 * q**2 - (q**2-1)*(1+m**2) ) ) / (1+m**2)
    #  dx = xA-xB
    #  dy = m*dx
    #  ==> dx = 2 * (sqrt( m**2 * q**2 - (q**2-1)*(1+m**2))) / (1+m**2)
    m2 = m**2
    q2 = q**2
    dx = np.multiply(2, np.sqrt( m2 * q2 - (q2-1)*(1+m2) ) ) / (1+m2) 

    #Chord length = sqrt( (xA-xB)**2 + (yA-yB)**2)
    return np.sqrt( (1+m2) * dx**2 )

def plot_chord_distribution(chords, title='chord_distribution.pdf'):
    pass

def two_points_on_circumference(samples=10000000, seed=42):
    """
    Given two random points on the circumference of a (unit) circle, it computes the
    probability that the length of the chord is
    bigger than the side of the equilateral triangle
    inscribed in the circle.
    """
    print "Generate pairs of points on a circumference with equilateral triangle inscribed..."
    #Set seed
    rn.seed(seed)
    #The side of the triangle is 2*r*cos30 = 2*r*sqrt(3)/2 = sqrt(3) (r=1)
    side = sqrt(3)
    print "Side of triangle: %f" % side 
    #Uniform angles correspond to uniform points on the circumference
    angles = rn.uniform(0.,2.*pi,samples)
    #Get length of all chords corresponding to the angles
    chords = np.array( map(angle_to_chord, angles ) )
    #Compute probability and (binomial) uncertainty
    passed = chords > side
    prob, prob_err = get_binomial_prob(passed, samples)
    print "Probability to have chords>side of triangle:" 
    print "%lf +/- %lf" % (prob, prob_err)
    print "(expected = 1/3)"

def random_midpoint(samples=10000000, seed=42):
    """
    """
    print "Generate chords by selecting random midpoints in circle with equilateral triangle inscribed..."
    #Set seed
    rn.seed(seed)
    #The side of the triangle is 2*r*cos30 = 2*r*sqrt(3)/2 = sqrt(3) (r=1)
    side = sqrt(3)
    print "Side of triangle: %f" % side
    #Uniform radii correspond to uniform points inside the circle
    midpoints = np.array( map(sqrt, rn.uniform(0.,1.0,samples)) )
    #Get corresponding chord length
    chords = np.array( map(midpoint_to_chord, midpoints) )
    #Compute probability and (binomial) uncertainty
    passed = chords > side
    prob, prob_err = get_binomial_prob(passed, samples)
    print "Probability to have chords>side of triangle:"
    print "%lf +/- %lf" % (prob, prob_err)
    print "(expected = 1/4)"

def two_points_in_circle(samples=10000000, seed=42):
    """
    """
    print "Generate chords by selecting random pairs of points inside circle with equilateral triangle inscribed..."
    #Set seed
    rn.seed(seed)
    #The side of the triangle is 2*r*cos30 = 2*r*sqrt(3)/2 = sqrt(3) (r=1)
    side = sqrt(3)
    print "Side of triangle: %f" % side
    #Generate uniform angles
    angles1 = rn.uniform(0.,2.*pi,samples)
    angles2 = rn.uniform(0.,2.*pi,samples)
    #Generate uniform radii (generate r^2, pick up r)
    radii1 = np.array( map(sqrt, rn.uniform(0.,1.0,samples)) )
    radii2 = np.array( map(sqrt, rn.uniform(0.,1.0,samples)) )
    #Compute lenghts
    chords = get_chord_from_int_points(radii1, angles1, radii2, angles2)
    #Compute probability and (binomial) uncertainty
    passed = chords > side
    prob, prob_err = get_binomial_prob(passed, samples)
    print "Probability to have chords>side of triangle:"
    print "%lf +/- %lf" % (prob, prob_err)

if __name__ == "__main__":
    two_points_on_circumference()
    random_midpoint()
    two_points_in_circle(samples=1)
