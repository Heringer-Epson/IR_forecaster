#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
from itertools import cycle
from preprocess_data import Preproc_Data

mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
fs = 24.

c = ['#377eb8','#4daf4a','#984ea3','#ff7f00',
           '#a65628','#f781bf']

def get_label(first_dates, last_dates):

    first_years = first_dates.astype('datetime64[Y]').astype(int) + 1970
    first_months = first_dates.astype('datetime64[M]').astype(int) % 12 + 1
    last_years = last_dates.astype('datetime64[Y]').astype(int) + 1970
    last_months = last_dates.astype('datetime64[M]').astype(int) % 12 + 1

    N = len(first_years)
    return [
      str(first_years[i]) + '-' + str(first_months[i]) + ' to ' +
      str(last_years[i]) + '-' + str(last_months[i]) for i in range(N)]
    

class Plot_Structure(object):
    """
    Description:
    ------------
    TBW.

    Parameters:
    -----------
    TBW.

    Outputs:
    --------
    ./../OUTPUTS/term_structure_X.pdf (where X is a currency).
    """        
    def __init__(self, M, tenor, incr, outdir):
        
        self.M = M
        self.tenor = tenor
        self.incr = incr
        self.outdir = outdir
        
        self.D = {}
        self.df = None 

        self.fig, self.ax = plt.subplots(1,1, figsize=(12,8))
        
    def merge_data(self):
        #Merge data such that a dictionary entry for increment contain columns
        #for different tenors.
        for incr in self.incr:
            
            aux = pd.merge(
              self.M['1m_'], self.M['3m'], how='inner', on='date',
              suffixes=['_1m', '_3m'])
            self.df = pd.merge(aux, self.M['12m'], how='inner', on='date')
            self.df = self.df.rename(columns={'ir': 'ir_12m'})
            #Data should already be clean by now, but add an extra step.
            self.df = self.df.dropna() 
    
    def set_fig_frame(self):
 
        #plt.subplots_adjust(left=.12, right=.97, bottom=0., top=0.92)
        self.ax.set_xlabel(r'Maturity [months]', fontsize=fs)
        self.ax.set_ylabel(r'yield [%]', fontsize=fs)
        self.ax.set_xlim(0.,13.)
        #self.ax.set_ylim(0.,4.)
        self.ax.tick_params(axis='y', which='major', labelsize=fs, pad=8)      
        self.ax.tick_params(axis='x', which='major', labelsize=fs, pad=8)
        self.ax.tick_params('both', length=12, width=2., which='major',
                             direction='in', right=True, top=True)
        self.ax.tick_params('both', length=6, width=2., which='minor',
                             direction='in', right=True, top=True) 
        self.ax.xaxis.set_minor_locator(MultipleLocator(1.))
        self.ax.xaxis.set_major_locator(MultipleLocator(3.))
        #self.ax.yaxis.set_minor_locator(MultipleLocator(.25))
        #self.ax.yaxis.set_major_locator(MultipleLocator(1.))
          
    def add_monthly_structures(self):
        #Use the collection of IRs averaged over months.
        #One line per monthly average.
        list_of_monthly_IR = [self.M[str(tenor) + 'm_25d'].ir_mean.values
                              for tenor in self.tenor]
        transposed_list = list(map(np.array, zip(*list_of_monthly_IR)))

        for IRs in transposed_list:            
            self.ax.plot(
              self.tenor, IRs, ls='-', lw=1., marker='None', color='gray',
              alpha=0.25)

    def add_yearly_structures(self):
        #Use the collection of IRs averaged over years.
        #One line per yearly average.
        yearly_IR = [self.M[str(tenor) + 'm_253d'].ir_mean.values
                     for tenor in self.tenor]
        y_list = list(map(np.array, zip(*yearly_IR)))

        yearly_IR_std = [self.M[str(tenor) + 'm_253d'].ir_std.values
                         for tenor in self.tenor]
        yerr_list = list(map(np.array, zip(*yearly_IR_std)))

        labels = get_label(self.M['1m_253d'].first_date.values,
                           self.M['1m_253d'].last_date.values)

        for i, (IR, IRerr) in enumerate(zip(y_list, yerr_list)):            
            self.ax.errorbar(
              self.tenor, IR, yerr=IRerr, ls='--', lw=4., marker='^',
              markersize=12., color=c[i], label=labels[i])

    def add_average_structures(self):
        IR_avg = [np.mean(self.M[str(tenor) + 'm_1d'].ir_mean.values)
                  for tenor in self.tenor]
        IR_std = [np.std(self.M[str(tenor) + 'm_1d'].ir_mean.values)
                  for tenor in self.tenor] 
        self.ax.errorbar(
          self.tenor, IR_avg, yerr=IR_std, ls='-', lw=4., marker='s',
          markersize=12., color='k')

    def make_legend(self):
        self.ax.plot(
          [np.nan], [np.nan], ls='-', marker='s', markersize=12., lw=4.,
          color='k', label=r'All Data')   
        self.ax.plot(
          [np.nan], [np.nan], ls='-', marker='None', lw=1., color='gray',
          alpha=0.5, label=r'Monthly')     
        self.ax.legend(
          frameon=False, fontsize=fs, labelspacing=.1, numpoints=1, loc=2,
          ncol=2, handlelength=1.5, title_fontsize=fs)         

    def manage_output(self):
        fname = 'Fig_term_structure.pdf'
        plt.savefig(os.path.join(self.outdir, fname), format='pdf')
        plt.close(self.fig)    

    def make_plot(self):
        self.set_fig_frame()
        self.add_monthly_structures()
        self.add_yearly_structures()
        self.add_average_structures()
        self.make_legend()
        self.manage_output() 
