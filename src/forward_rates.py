#!/usr/bin/env python

import numpy as np

class Forward_Rates(object):
    """
    Description:
    ------------
    TBW.

    Parameters:
    -----------
    TBW.

    Outputs:
    --------
    ./../OUTPUTS/RUNS/Fig_corr.pdf
    """        
    def __init__(self, X_0, fit, model, random_array):
        self.X_0 = X_0
        self.fit = fit
        self.model = model
        self.random_array = random_array
        
        self.model_func = None
        self.X_forward = None

    def retrieve_function(self):
        dt = 1./253.
        
        if self.model == 'Brownian':
            mu, sigma = self.fit[0], self.fit[1]
            step = np.exp((mu - sigma**2./2.)*dt
                          + sigma*self.random_array)
            self.X_forward = [self.X_0] + list(self.X_0 * step.cumprod())    
            #self.X_forward = self.X_0 * np.cumprod(step)    

        if self.model == 'Vasicek':
            theta1, theta2, theta3 = self.fit[0], self.fit[1], self.fit[2]
            self.X_forward = [self.X_0]
            for i in range(len(self.random_array)):
                self.X_forward.append(
                  theta1*(theta2 - self.X_forward[i])
                  + theta3*self.random_array[i]) #np.cumsum
            
    def run(self):
        self.retrieve_function()
        return self.X_forward
