#!/usr/bin/env python

import numpy as np
from sklearn.decomposition import PCA

class Explained_Var(object):
    """
    Description:
    ------------
    Given a matrix of IR values, compute the explained variance as a function
    of number of principal components.

    Parameters:
    -----------
    matrix : ~list of lists.
        Matrix containing the IR (or transformed IR values). Each row in the
        correspodents to a date and each column to a tenor.
 
    Return:
    -------
    n_pca_array: numpy array with number of tested PCs.
    exp_var: the percent explained variance for each tested PC.  

    """         
    def __init__(self, matrix):
        self.matrix = matrix
        
        self.N_pca = matrix.shape[1] - 1 #Maximum of PC = number of tenors -1.
        self.n_pca_array = np.arange(1,self.N_pca,1)
        self.exp_var = None

    def run(self):
        pca = PCA(n_components=self.N_pca)
        pca.fit(self.matrix) 
        self.exp_var = np.cumsum(pca.explained_variance_ratio_)
        return self.n_pca_array, self.exp_var
