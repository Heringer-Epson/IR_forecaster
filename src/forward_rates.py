#!/usr/bin/env python

import numpy as np
from pars import Inp_Pars

class Forward_Rates(object):
    """
    Description:
    ------------
    For a given fitted financial model, compute a realization of future
    IRs (or transformed IRs).

    Parameters:
    -----------
    X_0 : ~float
        The current IR (or transformed IR).
    fit : ~list of floats
        A list containing the fits for the financial model to be used.
    model : ~str
        Specifies which financial model to use.
    random_array : np.array
        Array containing a sequence of random numbers to compute future rates.

    Notes:
    ------
    The number of steps is implicitly determined by the size of random_array.

    Return:
    -------
    X_forward: An array containing a realization of future rates.
    """         
    def __init__(self, X_0, fit, model, random_array):
        self.X_0 = X_0
        self.fit = fit
        self.model = model
        self.random_array = random_array
        
        self.model_func = None
        self.X_forward = None

    def retrieve_function(self):       
        if self.model == 'Brownian':
            mu, sigma = self.fit[0], self.fit[1]
            step = np.exp((mu - sigma**2./2.)*Inp_Pars.dt
                          + sigma*self.random_array)
            self.X_forward = [self.X_0] + list(self.X_0 * np.cumprod(step))    

        if self.model == 'Vasicek':
            theta1, theta2, theta3 = self.fit[0], self.fit[1], self.fit[2]
            self.X_forward = [self.X_0]
                        
            for i in range(len(self.random_array)):
                self.X_forward.append(
                  self.X_forward[i]
                  + theta1*(theta2 - self.X_forward[i])*Inp_Pars.dt
                  + theta3*self.random_array[i])
            
    def run(self):
        self.retrieve_function()
        return self.X_forward
