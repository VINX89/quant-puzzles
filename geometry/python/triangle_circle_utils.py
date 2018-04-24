#!/usr/bin/env python
import os, sys
import numpy as np
from numpy import random as rn
from math import sqrt, sin, cos, pi
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def angle_to_chord(angle):
    """Compute length of chord associated
    to a given angle in the unit circle
    @param angle angle
    @return chord length
    """
    return 2.*sin(angle/2.)

def midpoint_to_chord(midpoint):
    """Compute lenght of chord
    given the distance of the midpoint
    from the center of the (unit) circle
    @param midpoint distance of the midpoint from the center
    @return chord length
    """
    return 2.*sqrt(1. - midpoint**2)

def get_chord_from_int_points(rho1, theta1, rho2, theta2):
    """Compute lenght of chord (in the unit circle) given the polar
    coordinates of two points in the circle. The points belongs two the chord.
    @param rho1 first point rho coordinate
    @param theta1 first point theta coordinate
    @param rho2 second point rho coordinate
    @param theta2 second point theta coordinate
    @return chord length
    """

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


class Plotter(object):
    """Handler to plot the distribution
    of generated chords
    """
    def __init__(self):
        self.hist = []
        self.labels = []
        self.colors = []
        self.refs = []
        self.colors_ref = []
        self.__patches__ = []
    def __add_patch__(self, label, color):
        self.__patches__.append( mpatches.Patch(color=color, label=label, alpha=0.5) )
    def add_plot(self, data, label, color):
        self.hist.append( data )
        self.labels.append( label )
        self.colors.append( color )
        self.__add_patch__(label, color)
    def add_reference(self, ref, label, color):
        self.refs.append( ref )
        self.colors_ref.append( color )
        self.__add_patch__(label, color)
    def plot(self, bins, title):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #Plot distribution of chord length                                                                                                          
        for data, label, color in zip(self.hist, self.labels, self.colors):
            plt.hist(data, normed=True, color=color, bins=bins, alpha=0.5)
        for ref, color in zip(self.refs, self.colors_ref):
            plt.axvline(x=ref, color=color, alpha=0.5)
        plt.xlabel('chord length')
        plt.ylabel('a.u.')
        ax.legend(loc='best', handles=self.__patches__)
        fig.savefig(title)
        
