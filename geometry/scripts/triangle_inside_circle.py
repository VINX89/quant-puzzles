#!/usr/bin/env python
import os, sys
import numpy as np
from numpy import random as rn
from math import sqrt, sin, cos, pi
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.append("../python")
from triangle_circle_utils import angle_to_chord, midpoint_to_chord, get_chord_from_int_points, Plotter
from prob_utils import get_binomial_prob

def two_points_on_circumference(samples=10000000, seed=42):
    """Given two random points on the circumference of a (unit) circle, it computes the
    probability that the length of the chord is
    bigger than the side of the equilateral triangle
    inscribed in the circle.

    @param samples number of samples for the Monte Carlo generation
    @param seed seed for the Monte Carlo generation
    @return array with length of generated chords
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
    print "(expected = 1/3)"
    return chords

def random_midpoint(samples=10000000, seed=42):
    """Given a random point in the (unit) circle, it computes the probability that
    the lenght of the chord having this point as midpoint is bigger than
    than the side of the equilateral triangle inscribed in the circle.

    @param samples number of samples for the Monte Carlo generation                                                                    
    @param seed seed for the Monte Carlo generation                                                                                         
    @return array with length of generated chords
    """

    print "Generate chords by selecting random midpoints in circle with equilateral triangle inscribed..."
    #Set seed
    rn.seed(seed)
    #The side of the triangle is 2*r*cos30 = 2*r*sqrt(3)/2 = sqrt(3) (r=1)
    side = sqrt(3)
    print "Side of triangle: %f" % side
    #Uniform radii correspond to uniform points inside the circle
    midpoints = np.sqrt( rn.uniform(0.,1.0,samples) )
    #Get corresponding chord length
    chords = np.array( map(midpoint_to_chord, midpoints) )
    #Compute probability and (binomial) uncertainty
    passed = chords > side
    prob, prob_err = get_binomial_prob(passed, samples)
    print "(expected = 1/4)"
    return chords

def two_points_in_circle(samples=10000000, seed=42):
    """Given two random points in the (unit) circle, it computes the probability that
    the length of the chord passing through this pair of points is bigger than
    the side of the equilateral triangle inscribed in the circle

    @param samples number of samples for the Monte Carlo generation                                                                            
    @param seed seed for the Monte Carlo generation                                                                                                              
    @return array with length of generated chords
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
    return chords

if __name__ == "__main__":
    c1 = two_points_on_circumference()
    c2 = random_midpoint()
    c3 = two_points_in_circle()
    plotter = Plotter()
    plotter.add_plot(c1, '2 points on circumference', 'blue')
    plotter.add_plot(c2, 'random midpoint', 'red')
    plotter.add_plot(c3, '2 points inside circle', 'green')
    plotter.add_reference(sqrt(3), 'side of triangle', 'black')
    plotter.plot(40, 'plot.pdf')
