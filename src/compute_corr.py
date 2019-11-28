#!/usr/bin/env python

import sys
import os
import pandas as pd

from preprocess_data import Preproc_Data
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'webapp'))
import utils

class Compute_Corr(object):
    """
    Description:
    ------------
    Fix this!
    Given a set of tenors and increments, this package collects and preprocesses
    the IR data by applying the requested transformation and selecting only
    the desired time interval.

    Parameters:
    -----------
    curr : ~str
        Currency. 'USD' or 'CAD'. Default is 'USD'.
    incr : ~list of int
        List of increments. Value to be used when computing data transformations.
        E.g. if incr=[1,25], then a dataframe will be created for each increment:
        df_{1}[Diff.(IR)] = IR_{i + 1} - IR_{i}
        df_{25}[Diff.(IR)] = IR_{i + 25} - IR_{i}
        Default is [1,25].
    tenor : ~list of int
        List of tenors (in unit of months) to be used. For each element in the
        list, a dataframe will be created. Default is [1,2,3,6,12].
    application : ~str
        What sort of transformation to apply to the data. Options are:
            'simple_diff':  Calculate IR_{i + incr} - IR_{i}
            'log ratio':  Calculate natural log(IR_{i + incr} / IR_{i}).
        Default is 'simple_diff'
    t_ival : list of date strings
        List containing [date_min, date_max], such that only IRs in the selected
        range are included. Default is None.
    
    Return:
    -------
    A dictionary containing dataframes for each combination of requested tenors
    and increments.
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
