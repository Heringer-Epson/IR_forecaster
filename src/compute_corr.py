#!/usr/bin/env python

import os
import numpy as np
import pandas as pd

from preprocess_data import Preproc_Data

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

class Compute_Corr(object):
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
    def __init__(self, curr, tenor, incr, transf, t_range, application):
        self.curr = curr
        self.tenor = tenor
        self.incr = incr
        self.transf = transf
        self.t_range = t_range
        self.application = application
        
        self.curr_list, self.tenor_list, self.incr_list = None, None, None
        self.qtty = None
        
        self.list_M = []
        self.df = None
        self.corr_matrix = None
        self.columns = None

    def fix_variables(self):

        if self.curr == 'USD & CAD':
            self.curr_list = ['USD', 'CAD']
        else:
            self.curr_list = [self.curr]

        if self.incr == '1 & 25':
            self.incr_list = [1, 25]
        else:
            self.incr_list = [int(self.incr)]   

        if self.transf == 'Raw':
            self.qtty = 'ir'
        else:
            self.qtty = 'ir_transf'

    def collect_IRs(self):
        for curr in self.curr_list:
            self.list_M.append(
              Preproc_Data(curr=curr, incr=self.incr_list, t_ival=self.t_range,
                           application=self.application).run())

    def merge_dataframes(self):

        list_df = []
        for M, curr in zip(self.list_M,self.curr_list):
            for incr in self.incr_list:
                for t in self.tenor:
                    key = '{}m_{}d'.format(str(t),str(incr))
                    aux = M[key][['date',self.qtty]]
                    aux.set_index('date', inplace=True)
                    aux.rename(columns={
                      self.qtty:self.qtty + '_{}_{}m'.format(curr, str(t))}, inplace=True)
                    list_df.append(aux)
        self.df = pd.concat(list_df, axis=1, join='inner', ignore_index=False)
        self.df.index = pd.to_datetime(self.df.index)
         
    def get_matrix(self):
        
        self.corr_matrix = self.df.corr()
        self.columns = self.df.columns


        '''
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
        '''
 

    def run(self):
        self.fix_variables()
        self.collect_IRs()
        self.merge_dataframes()
        self.get_matrix()
        return self.corr_matrix, self.columns
