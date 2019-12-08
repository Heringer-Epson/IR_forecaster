import numpy as np
from sklearn.decomposition import PCA
from pars import Inp_Pars

class Compute_Pca(object):
    """
    Description:
    ------------
    TBW.

    Parameters:
    -----------
    TBW.
    """         
    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(Inp_Pars.PCA)
        
        self.pca = None
        self.eigenvalues = None
        
        self.decompose()
    
    def decompose(self):
        self.pca = PCA(n_components=self.n)
        self.pca.fit(self.matrix)
        self.components = self.pca.transform(self.matrix)
        self.eigenvalues = self.pca.explained_variance_
        
    #def run(self):
    #    self.decompose()
'''
if __name__ == '__main__':
    matrix = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    #matrix = np.array([[0, 1], [-2, -3]])
    #matrix = np.array([[0.7071068, 0.7071068], [-0.71711, 0.71711]])
    Compute_Pca(matrix).run()
'''        
