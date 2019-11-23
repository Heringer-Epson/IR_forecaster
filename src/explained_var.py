#!/usr/bin/env python

import numpy as np
from sklearn.decomposition import PCA

class Explained_Var(object):
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
    def __init__(self, merged_df):
        self.merged_df = merged_df
        
        self.N_pca = 5
        self.n_pca_array = np.arange(1,self.N_pca,1)
        self.exp_var = None

    def run(self):
        pca = PCA(n_components=self.N_pca)
        pca.fit(self.merged_df.values) 
        self.exp_var = np.cumsum(pca.explained_variance_ratio_)
        return self.n_pca_array, self.exp_var
