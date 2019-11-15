#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
from sklearn.decomposition import PCA

mpl.style.use('classic')
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
fs = 16.

def plot_scatter(X, X_proj, ax, cx, cy):
    ax.scatter(X[:,cx], X[:,cy], alpha=0.1, color='k')
    ax.scatter(X_proj[:,cx], X_proj[:,cy], alpha=0.8, color='k')
    ax.axis('equal')

    #Format plot
    ax.tick_params(axis='y', which='major', labelsize=fs, pad=8)      
    ax.tick_params(axis='x', which='major', labelsize=fs, pad=8)
    ax.tick_params('both', length=12, width=2., which='major',
                         direction='in', right=True, top=True)
    ax.tick_params('both', length=6, width=2., which='minor',
                         direction='in', right=True, top=True) 
    
    ax.set_xlabel(r'PCA {}'.format(str(cx + 1)), fontsize=fs)
    ax.set_ylabel(r'PCA {}'.format(str(cy + 1)), fontsize=fs)


class Plot_Pca(object):
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
    def __init__(self, M, curr, tenor, outdir):
        self.M = M
        self.curr = curr
        self.tenor = tenor
        self.outdir = outdir
        
        self.X, self.pca = {}, {}
        self.X['1'], self.X['25'] = [], []
        
        self.incr = [1,25]
        self.fig, self.ax = plt.subplots(2,3, figsize=(20,16))
          
    def prep_data(self):
        for incr in self.incr:
            for tenor in self.tenor:
                key = '{}m_{}d'.format(str(tenor), str(incr))
                self.X[str(incr)].append(self.M[key]['ir_transf_mean'].values)
            self.X[str(incr)] = np.transpose(self.X[str(incr)])

    def compute_pca(self):
        for incr in self.incr:
            pca = PCA(n_components=3)
            self.pca[str(incr)] = pca.fit(self.X[str(incr)])
                    
    def set_fig_frame(self):
        plt.subplots_adjust(left=.1, right=.95, bottom=.05, top=.95,
        wspace=.3, hspace=0.25)
        self.ax[0,0].text(
          -.35, .5, r'$\Delta t = 1\mathrm{d}$', rotation='vertical',
          transform=self.ax[0,0].transAxes, verticalalignment='center', 
          fontsize=fs + 10)
        self.ax[1,0].text(
          -.35, .5, r'$\Delta t = 25\mathrm{d}$', rotation='vertical',
          transform=self.ax[1,0].transAxes, verticalalignment='center', 
          fontsize=fs + 10)


    def plot_projections(self):
        
        for i, incr in enumerate(self.incr):
            X = self.X[str(incr)]
            pca = PCA(n_components=3)
            pca.fit(X)
            X_pca = pca.transform(X)
            X_proj = pca.inverse_transform(X_pca)
            
            plot_scatter(X, X_proj, self.ax[i, 0], 0, 1)     
            plot_scatter(X, X_proj, self.ax[i, 1], 0, 2)     
            plot_scatter(X, X_proj, self.ax[i, 2], 1, 2)     
         
         
            
    def manage_output(self):
        fpath = os.path.join(self.outdir, 'Fig_pca.pdf')
        plt.savefig(fpath, format='pdf')
        plt.close(self.fig)    

    def make_plot(self):
        self.prep_data()
        self.compute_pca()
        self.set_fig_frame()
        self.plot_projections()
        self.manage_output()

