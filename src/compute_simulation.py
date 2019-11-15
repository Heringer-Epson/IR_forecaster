#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
import copy
from scipy.linalg import cholesky

class Compute_Simulation(object):
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
    def __init__(self, M, application, tenor, incr, fit_coeffs, outdir):
        self.M = M
        self.application = application
        self.tenor = tenor
        self.incr = incr
        self.fit_coeffs = fit_coeffs
        self.outdir = outdir
        
        self.T_sim = None #Simulation period, in years.
        self.dt = None #Simulation time step.
        self.sqrt_st = None #square root of dt. Avoids repeating this calc.
        self.cM = None
        
        self.N_sim = 5
        self.r_fut = {}
        self.out = {}
        self.a, self.b, self.sigma = [], [], []
        
    def compute_parameters(self, incr):
        self.dt = 1./365.*incr
        self.T_sim = 1.
        self.sqrt_dt = np.sqrt(self.dt)
        self.t_steps = np.arange(self.dt, self.T_sim + 1.e-5, self.dt)
        
        for tenor in self.tenor:
            key = '{}m_{}d'.format(str(tenor), str(incr))
            self.a.append(self.fit_coeffs[key][0])        
            self.b.append(self.fit_coeffs[key][1])        
            self.sigma.append(self.fit_coeffs[key][2])        
    
        self.a = np.array(self.a)
        self.b = np.array(self.b)
        self.sigma = np.array(self.sigma)

        #Get initial values for future similation.
        self.r = [np.array([self.M['{}m_{}d'.format(str(tenor), str(incr))]\
                   ['ir_transf_mean'].values[-1] for tenor in self.tenor])]

        self.IR = [np.array([self.M['{}m_{}d'.format(str(tenor), str(incr))]\
                   ['ir_mean'].values[-1] for tenor in self.tenor])]

    def compute_corr_matrix(self, incr):
        aux = []
        for tenor in self.tenor:
            key = '{}m_{}d'.format(str(tenor), str(incr))
            aux.append(self.M[key]['ir_transf_mean'].values)
        aux = np.asarray(aux)
        corr_matrix = np.corrcoef(aux)
        self.dec = cholesky(corr_matrix, lower=False)

    def compute_dW(self):
        #dW = [dW_tenor1, dW_tenor2, dW_tenor3 ..., dW_tenorN]
        dW = np.random.normal(scale=self.sqrt_dt, size=len(self.tenor))
        dW_corr = np.dot(self.dec, dW)
        
        return dW_corr
        

    def next_step(self):
        
        for i_sim in range(self.N_sim):
            r_sim = copy.deepcopy(self.r)
            
            for j in range(len(self.t_steps)): 
            #for j in range(10): 
            
                dW = self.compute_dW()
                dr = self.a*(self.b - r_sim[j])*self.dt + self.sigma*dW
                r_sim.append(r_sim[j] + dr)
            self.r_fut[str(i_sim)] = np.asarray(r_sim)
                  
    def transform_data_to_IR(self):
        if self.application == 'simple_diff':
            for i_sim in range(self.N_sim):
                self.out[str(i_sim)] = self.IR + self.r_fut[str(i_sim)]

        elif self.application == 'log_ratio':
            for i_sim in range(self.N_sim):
                self.out[str(i_sim)] = self.IR*10.**self.r_fut[str(i_sim)]
        else:
            raise ValueError(
              'Application %s is not supported' %self.application)                
        print(self.out['1'])

    def make_plot(self):
        for incr in self.incr:
        
            self.compute_parameters(incr)
            self.compute_corr_matrix(incr)
            self.next_step()
            self.transform_data_to_IR()
            return self.out

