#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from matplotlib.ticker import MultipleLocator

sns.set(style='white')
sns.set(font_scale=2.5)
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
fs = 24.

def add_corr(df, ax, cmap):
    #For an example, see:
    #https://seaborn.pydata.org/examples/many_pairwise_correlations.html
    
    corr = df.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    
    im = sns.heatmap(
      corr, mask=mask, cmap=cmap, vmax=1., vmin=-1., center=0,
      square=False, linewidths=2., ax=ax, cbar=False)

    #The setting of ylim in seaborn heatmap is broken with matplotlib 3.1.0
    #and 3.1.1, set this manually.
    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)
    return im

class Plot_Corr(object):
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
        
        self.incr = [1,25]
        self.fig, self.ax = plt.subplots(1,2, figsize=(20,8))
          
        self.df1, self.df25 = pd.DataFrame({}), pd.DataFrame({})

    def prep_data(self):
        for incr in self.incr:
            for tenor in self.tenor:
                key = '{}m_{}d'.format(str(tenor), str(incr))
                self.M[key] = self.M[key][['first_date', 'ir_transf_mean']]
                self.M[key].rename(columns={
                  'ir_transf_mean':'{}m'.format(str(tenor))},
                  inplace=True)

    def get_plotting_df(self):
        aux1 = self.M[str(self.tenor[0]) + 'm_1d'].copy(deep=True)
        aux25 = self.M[str(self.tenor[0]) + 'm_25d'].copy(deep=True)
        
        for tenor in self.tenor[1:]:
            key = str(tenor) + 'm_1d'
            aux1 = pd.merge(aux1, self.M[key], how='left', on='first_date')
            aux25 = pd.merge(aux25, self.M[key], how='left', on='first_date')
        self.df1, self.df25 = aux1, aux25
            
    def set_fig_frame(self):
        plt.subplots_adjust(right=0.8, wspace=.2)
         
    def plot_corr_matrix(self):
        
        #Remove the non-numeric column.
        del self.df1['first_date']    
        del self.df25['first_date'] 

        cmap = sns.diverging_palette(220, 10, as_cmap=True)        
        add_corr(self.df1, self.ax[0], cmap)
        add_corr(self.df25, self.ax[1], cmap)

        cbar_ax = self.fig.add_axes([0.85, 0.1, 0.02, 0.8])
        
        norm = mpl.colors.Normalize(vmin=-1., vmax=1.)
        cb = mpl.colorbar.ColorbarBase(
          cbar_ax, cmap=cmap, norm=norm)
          
        #Set subplot titles.
        self.ax[0].set_title('1 day increment', fontsize=fs)
        self.ax[1].set_title('25 day increment', fontsize=fs)
        self.fig.suptitle('Currency: {}'.format(self.curr), fontsize=fs)
        

    def manage_output(self):
        fpath = os.path.join(self.outdir, 'Fig_corr.pdf')
        plt.savefig(fpath, format='pdf')
        plt.close(self.fig)    

    def make_plot(self):
        self.prep_data()
        self.get_plotting_df()
        self.set_fig_frame()
        self.plot_corr_matrix()
        self.manage_output()

