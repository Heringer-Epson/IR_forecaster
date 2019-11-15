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

c = ['#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']
ls = ['-', '--']
marker = ['s', '^', 'o', 'H']

def make_key(tenor, incr):
    return tenor + '_' + str(incr)

class Ir_Std(object):
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
    def __init__(self, M, tenor, incr, outdir, mode):
        
        self.M = M
        self.tenor = tenor
        self.incr = incr
        self.outdir = outdir
        self.mode = mode
        self.std = {}
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2,1, figsize=(12,8))
    
    def set_fig_frame(self):
 
        plt.subplots_adjust(left=.12, right=.97, top=0.92, hspace=0.1)
       
        self.ax1.set_ylabel(r'$\sigma_{1\mathrm{d}}~/~\sigma_{25\mathrm{d}}$',
                            fontsize=fs)
        self.ax1.set_xlim(0.,13.)
        #self.ax1.set_ylim(.5,1.5)
        self.ax1.tick_params(axis='y', which='major', labelsize=fs, pad=8)      
        self.ax1.tick_params(axis='x', which='major', labelsize=fs, pad=8)
        self.ax1.tick_params('both', length=12, width=2., which='major',
                             direction='in', right=True, top=True)
        self.ax1.tick_params('both', length=6, width=2., which='minor',
                             direction='in', right=True, top=True) 
        self.ax1.xaxis.set_minor_locator(MultipleLocator(1.))
        self.ax1.xaxis.set_major_locator(MultipleLocator(3.))
        #self.ax1.yaxis.set_minor_locator(MultipleLocator(.1))
        #self.ax1.yaxis.set_major_locator(MultipleLocator(.5))
        self.ax1.tick_params(labelbottom=False) 

        self.ax2.set_xlabel(r'Maturity [months]', fontsize=fs)
        self.ax2.set_ylabel(r'$\sigma$', fontsize=fs)
        self.ax2.set_xlim(0.,13.)
        #self.ax2.set_ylim(0.,1.)
        self.ax2.tick_params(axis='y', which='major', labelsize=fs, pad=8)      
        self.ax2.tick_params(axis='x', which='major', labelsize=fs, pad=8)
        self.ax2.tick_params('both', length=12, width=2., which='major',
                             direction='in', right=True, top=True)
        self.ax2.tick_params('both', length=6, width=2., which='minor',
                             direction='in', right=True, top=True) 
        self.ax2.xaxis.set_minor_locator(MultipleLocator(1.))
        self.ax2.xaxis.set_major_locator(MultipleLocator(3.))
        #self.ax2.yaxis.set_minor_locator(MultipleLocator(.05))
        #self.ax2.yaxis.set_major_locator(MultipleLocator(.25))

    def calculate_std(self):
        for incr in self.incr:
            self.std[str(incr)] = np.array([
              np.std(self.M[str(tenor) + 'm_' + str(incr) + 'd']\
              [self.mode + '_mean'].values) for tenor in self.tenor])        
          
    def plot_std(self):
        #For a given increment, compute the standard deviation of the mean
        #values.
        
        for i, incr in enumerate(self.incr):
            IR_std = self.std[str(incr)]
            self.ax2.plot(
              self.tenor, IR_std, ls='-', lw=4.,
              marker='^', color=c[i], markersize=12.,
              label=r'$\Delta t = ' + str(incr) + '\mathrm{d}$')

    def plot_std_ratio(self):
        try:
            IR_std_ratio = np.divide(self.std['1'], self.std['25'])
            self.ax1.plot(
              self.tenor, IR_std_ratio, ls='-', lw=4., marker='s', color='k',
              markersize=12.)
        except:
            raise ValueError(
              'Plot of std ratio as a funcction of maturity requires '\
              'increments of 1 and 25d.')

    def make_legend(self):      
        self.ax2.legend(
          frameon=False, fontsize=fs, labelspacing=.1, numpoints=1, loc=2,
          ncol=2, handlelength=2.5, title_fontsize=fs)         

    def manage_output(self):
        fname = 'Fig_{}_std.pdf'.format(self.mode)
        plt.savefig(os.path.join(self.outdir, fname), format='pdf')
        plt.close(self.fig)    

    def make_plot(self):
        self.set_fig_frame()
        self.calculate_std()
        self.plot_std()
        self.plot_std_ratio()
        self.make_legend()
        self.manage_output() 
