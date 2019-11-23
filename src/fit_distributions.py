#!/usr/bin/env python

import os
import math
import numpy as np
import pandas as pd
import scipy.stats

class Fit_Distr(object):
    """
    TBW.
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
            #print(pdf, pars)
            
            if not any([math.isnan(p) for p in pars]):
                arg = ', '.join([str(val) for val in pars])
                y_theor = eval(
                  'scipy.stats.' + pdf + '.pdf(xdom, '+ arg + ')')
     
                #Compute and print goodness of fit KS test.
                D, p = scipy.stats.kstest(self.y, pdf, args=pars)
                #print(pdf.ljust(18) + ('D: {}'.format(D).ljust(30))
                #      + ('p: {}'.format(p).ljust(45)))
            else:
                p = 0.
            
            self.fit_dict['y_' + pdf] = y_theor
            self.fit_dict['p_' + pdf] = p
            self.fit_dict['D_' + pdf] = D
        self.fit_dict['x'] = xdom
        
    def run_fitting(self):
        self.compute_histogram()
        self.make_pdf_list()
        self.make_fits()
        return self.hist, self.bins, self.fit_dict, self.pdfs
