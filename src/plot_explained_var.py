#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
from sklearn.decomposition import PCA

mpl.style.use('classic')
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
fs = 24.

class Plot_Expvar(object):
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
    def __init__(self, M, tenor, outdir):
        self.M = M
        self.tenor = tenor
        self.outdir = outdir
        
        self.X, = {}
        self.X['1'], self.X['25'] = [], []
        
        self.incr = [1,25]
        self.fig, (self.ax1, self.ax2) = plt.subplots(1,2, figsize=(14,8))
          
    def prep_data(self):
        for incr in self.incr:
            for tenor in self.tenor:
                key = '{}m_{}d'.format(str(tenor), str(incr))
                self.X[str(incr)].append(self.M[key]['ir_transf_mean'].values)
            self.X[str(incr)] = np.transpose(self.X[str(incr)])

    def set_fig_frame(self):
        plt.subplots_adjust(left=0.15, wspace=0.1)

        for incr, ax, in zip(self.incr, [self.ax1, self.ax2]):
            pca = PCA(n_components=5)
            pca.fit(self.X[str(incr)])  

            ax.set_xlim(0.,6.)
            ax.set_ylim(0.65,1.05)
            ax.tick_params(axis='y', which='major', labelsize=fs, pad=8)      
            ax.tick_params(axis='x', which='major', labelsize=fs, pad=8)
            ax.tick_params('both', length=12, width=2., which='major',
                                 direction='in', right=True, top=True)
            ax.tick_params('both', length=6, width=2., which='minor',
                                 direction='in', right=True, top=True) 
            ax.xaxis.set_major_locator(MultipleLocator(1.))
            ax.yaxis.set_minor_locator(MultipleLocator(.05))
            ax.yaxis.set_major_locator(MultipleLocator(.1))

        self.ax2.tick_params(labelleft=False) 
        self.ax1.set_ylabel(r'Explained Variance [%]', fontsize=fs)
        self.ax1.set_xlabel(r'Number of Components in PCA', fontsize=fs)
        self.ax2.set_xlabel(r'Number of Components in PCA', fontsize=fs)

    def plot_explained_variance(self):
        x = np.arange(1,6,1)
        for incr, ax, in zip(self.incr, [self.ax1, self.ax2]):
            pca = PCA(n_components=5)
            pca.fit(self.X[str(incr)])  
            ax.plot(
              x, np.cumsum(pca.explained_variance_ratio_), ls='-', lw=4.,
              color='k', marker='s', markersize=12.,
              label=r'$\Delta t = ' + str(incr) + ' \mathrm{d}$')   
            ax.legend(
              frameon=False, fontsize=fs, numpoints=1, loc=4, handlelength=1.5)        
         
    def manage_output(self):
        fpath = os.path.join(self.outdir, 'Fig_explained_var.pdf')
        plt.savefig(fpath, format='pdf')
        plt.close(self.fig)    

    def make_plot(self):
        self.prep_data()
        self.set_fig_frame()
        self.plot_explained_variance()
        self.manage_output()
