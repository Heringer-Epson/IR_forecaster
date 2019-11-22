#!/usr/bin/env python

import sys
import os
import numpy as np
import pandas as pd

from preprocess_data import Preproc_Data

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'webapp'))
import utils

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
    def __init__(self, currtag='USD', tenor=[1,2,3,6,12], incrtag='1',
                 transf='Raw', t_range=None):
        self.currtag = currtag
        self.tenor = tenor
        self.incrtag = incrtag
        self.transf = transf
        self.t_range = t_range
                
        self.df = None
        self.corr_matrix = None
        self.columns = None           

    def merge_dataframes(self):

        curr_list = utils.currtag2curr[self.currtag]
        incr_list = utils.incrtag2incr[self.incrtag]
        qtty = utils.transf2IR[self.transf]   

        list_df = []
        for curr in curr_list:
            M = Preproc_Data(
              curr=curr, incr=incr_list, tenor=self.tenor,
              t_ival=self.t_range).run()
            for incr in incr_list:
                for t in self.tenor:
                    key = '{}m_{}d'.format(str(t),str(incr))
                    aux = M[key][['date',qtty]]
                    aux.set_index('date', inplace=True)
                    aux.rename(columns={
                      qtty:qtty + '_{}_{}m_{}d'.format(
                      curr, str(t), str(incr))}, inplace=True)
                    list_df.append(aux)
        self.df = pd.concat(list_df, axis=1, join='inner', ignore_index=False)
        self.df.index = pd.to_datetime(self.df.index)
         
    def get_matrix(self):
        self.corr_matrix = self.df.corr()
        self.columns = self.df.columns 

    def run(self):
        self.merge_dataframes()
        self.get_matrix()
        return self.corr_matrix, self.columns
