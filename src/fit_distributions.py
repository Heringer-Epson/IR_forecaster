#!/usr/bin/env python

import math
import numpy as np
import scipy.stats

class Fit_Distr(object):
    """
    Description:
    ------------
    Given an array of values, fit several pdfs to their histogram.

    Parameters:
    -----------
    y : ~np.array
        Array of values to be fitted, IRs or transformed IRs.
 
    Return:
    -------
    hist: The histogram of y.
    bins: The centered bins for the histogram of y.
    fit_dict: A dictionary containing properties of each of the fitted pdfs.
    pdfs: The list of fitted pdfs.
    """    
    def __init__(self, y):
        self.y = y
        
        self.hist = None
        self.bins = None
        self.pdfs = None
        self.fit_dict = {}
        
    def compute_histogram(self):
        self.hist, bins = np.histogram(self.y, bins=40, density=True)
        self.bins = (bins[1:] + bins[:-1])/2.
    
    def make_pdf_list(self):
        self.pdfs = ['norm', 'dweibull', 'expon', 'logistic', 'laplace',
                     'powerlaw', 'uniform']
        if all(self.y > 0.):
            self.pdfs += ['gamma', 'lognorm', 'exponweib',
                          'halflogistic', 'halfnorm']

    def make_fits(self):
        #Based on example from:
        #http://www.aizac.info/simple-check-of-a-sample-against-80-distributions/

        #Create a domain of x values for plotting the fitted distributions.
        xdom = np.linspace(min(self.y), max(self.y), len(self.y)) 

        for pdf in self.pdfs:
            
            #Fit distribution and get most likely parameters.
            pars = eval('scipy.stats.' + pdf + '.fit(self.y)')
            
            if not any([math.isnan(p) for p in pars]):
                arg = ', '.join([str(val) for val in pars])
                rng_expr = 'scipy.stats.' + pdf + '.rvs(' + arg + ', size='
                y_theor = eval(
                  'scipy.stats.' + pdf + '.pdf(xdom, '+ arg + ')')
     
                #Compute goodness of fit using KS test.
                D, p = scipy.stats.kstest(self.y, pdf, args=pars)
            else:
                p = 0.
            
            self.fit_dict['y_' + pdf] = y_theor
            self.fit_dict['rng_' + pdf] = rng_expr
            self.fit_dict['p_' + pdf] = p
            self.fit_dict['D_' + pdf] = D
        self.fit_dict['x'] = xdom
        
    def run_fitting(self):
        self.compute_histogram()
        self.make_pdf_list()
        self.make_fits()
        return self.hist, self.bins, self.fit_dict, self.pdfs
