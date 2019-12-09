from sklearn.decomposition import PCA
from pars import Inp_Pars

class Compute_Pca(object):
    """
    Description:
    ------------
    This routine is used to convert a matrix of IR rates to PCA space.

    Parameters:
    -----------
    matrix : ~numpy-matrix
        Matrix of IR rates. Rows correspond to different dates and columns to
        the multiple tenors.    
    """         
    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(Inp_Pars.PCA)
        self.pca = None
        
        self.decompose()
    
    def decompose(self):
        self.pca = PCA(n_components=self.n)
        self.pca.fit(self.matrix)
        self.pca_matrix = self.pca.transform(self.matrix) #Rename this...
        #self.components_ = self.pca.components_
        #self.explained_variance_ = self.pca.explained_variance_

