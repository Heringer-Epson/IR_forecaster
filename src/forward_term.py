#!/usr/bin/env python

import numpy as np
import scipy.stats
from scipy.linalg import cholesky

from pars import Inp_Pars
from fit_simpars import Fit_Simpars
from forward_rates import Forward_Rates

class Forward_Term(object):
    """
    Description:
    ------------
    Calculates a set of realizations (paths) for future IRs.

    Parameters:
    -----------
    matrix : ~matrix
        A Matrix containing IRs (or transformed IRs). Each row corresponds to
        a tenor and each column to a date.
    model : ~str
        Specifies which financial model to use.
    transf : ~str
        Specifies what IR to use. Can be 'Diff.', 'Log ratio' or 'Raw'. 
    rng_expr : ~list
        A list containing expressions that are used to generate random numbers.
        The expressions have been derived for each tenor and need to be
        called using eval.
    current_IR : ~list
        List containing the current IR (or transformed IR) for each tenor.
    guess : ~str
        A string containing the initial guess parameters for the taget model.
    ndays : ~int
        Number of days to be simulated.
    npaths : ~int
        Number of paths to be simulated. Default is set in the pars.py file.  

    Notes:
    ------
    The number of steps is implicitly determined by the size of random_array.

    Return:
    -------
    paths: A list of IR future paths, and lists containg the mean and std
    of such paths. 
    """           
    def __init__(self, matrix, model, transf, rng_expr, current_IR, guess,
                 ndays, npaths=Inp_Pars.MC_npaths):
        self.matrix = matrix
        self.model = model
        self.transf = transf
        self.rng_expr = rng_expr
        self.current_IR = current_IR
        self.guess = guess
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
            self.fit.append(Fit_Simpars(X, self.model, self.guess).run())
        #print(self.fit)

    def calculate_corr_matrix(self):
        corr_matrix = np.corrcoef(self.matrix)
        self.dec = cholesky(corr_matrix, lower=False)

    def generate_random(self):
                        
        #For a given path, produce a matrix of random numbers, where rows
        #correspond to different days and columns to different tenors.
        #For each column, the RN are drawn from the distribution that best
        #Fitted the IR (or IR_transf) of that tenor.
        def produce_random():           
            rdm_for_onepath = [eval(self.rng_expr[i] + str(self.ndays) + ')')
                               for i in range(self.Nt)]
            return np.transpose(rdm_for_onepath)

        #For each path, use the function above to draw random numbers (RN),
        #such that self.random_number[npaths][ndays][ntenor]
        self.random_number = [np.dot(produce_random(), self.dec) 
                              for j in range(self.npaths)]
    
    def calculate_forward(self):
        for i in range(self.Nt): #loop over tenor
            X_0 = self.matrix[i][-1]
            random_numbers = np.zeros(self.npaths)
            self.paths[str(i)] = np.array([Forward_Rates(
              X_0, self.fit[i], self.model, np.transpose(
              self.random_number[j])[i]).run() for j in range(self.npaths)])

    def convert_IR(self):
        if self.transf == 'Diff.':
            for i in range(self.Nt): #loop over tenor
                for j in range(self.npaths):
                    self.paths[str(i)][j] += self.current_IR[i]

        elif self.transf == 'Log ratio':
            for i in range(self.Nt): #loop over tenor
                for j in range(self.npaths):
                    self.paths[str(i)][j] = self.current_IR[i] * np.exp(self.paths[str(i)][j])             
            
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
        self.calculate_forward()
        self.convert_IR()
        self.prepare_output()
        return self.paths, np.transpose(self.mean).tolist(), np.transpose(self.std).tolist()
