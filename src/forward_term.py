#!/usr/bin/env python

import numpy as np
from scipy.linalg import cholesky

from fit_simpars import Fit_Simpars
from forward_rates import Forward_Rates

class Forward_Term(object):
    """
    Description:
    ------------
    TBW.

    Parameters:
    -----------
    TBW.
    """        
    def __init__(self, matrix, model, distr, ndays, npaths=10):
        self.matrix = matrix
        self.distr = distr
        self.model = model
        self.ndays = ndays
        self.npaths = npaths
        
        self.Nt = self.matrix.shape[0] #Number of tenors 
        
        self.dec = None
        self.random_number = None
        self.fit = []
        self.mean, self.std = [], []
        self.paths = {}

    def get_fit_pars(self):
        for X in self.matrix:
            self.fit.append(Fit_Simpars(X, self.model).run())

    def calculate_corr_matrix(self):
        corr_matrix = np.corrcoef(self.matrix)
        self.dec = cholesky(corr_matrix, lower=False)

    def generate_random(self):
        dt = 1./253.
        scale = np.sqrt(dt)
                        
        #For each path, calculate a matrix of correlated random numbers, where
        #nrows = ndays and ncols=ntenors. If there is only only tenor, the
        #Correlation does not matter.
        #self.random_number[npaths][ndays][ntenor]
        self.random_number = [
          np.dot(np.random.normal(0., scale, (self.ndays,self.Nt)), self.dec) 
          for j in range(self.npaths)]
    
    def calculate_paths(self):
        for i in range(self.Nt): #loop over tenor
            X_0 = self.matrix[i][-1]
            random_numbers = np.zeros(self.npaths)
            self.paths[str(i)] = [Forward_Rates(
              X_0, self.fit[i], self.model, np.transpose(self.random_number[j])[i]).run() for j in range(self.npaths)]
            
    def prepare_output(self):
        #Make output matrix where each row is a day and columns store the
        #mean and standard deviation for each term.
        #self.paths[tenor][npaths][ndays]
        #self.paths[tenor][ndays][npaths] #After transposing.
        for j in range(self.Nt):
            aux_mat = np.transpose(self.paths[str(j)])
            self.mean.append([np.mean(aux_mat[i]) for i in range(self.ndays)])
            self.std.append([np.std(aux_mat[i]) for i in range(self.ndays)])
    
    def run(self):
        self.get_fit_pars()
        self.calculate_corr_matrix()
        self.generate_random()
        self.calculate_paths()
        self.prepare_output()
        return self.paths, np.transpose(self.mean).tolist(), np.transpose(self.std).tolist()
