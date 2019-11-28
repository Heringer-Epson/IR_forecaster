#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter 

class Preproc_Data(object):
    """
    Description:
    ------------
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
    def __init__(self, curr='USD', incr=[1,25], tenor=[1,2,3,6,12],
                 application='simple_diff', t_ival=None):        
        self.curr = curr
        self.incr = incr
        self.tenor = tenor
        self.application = application
        self.t_ival = t_ival
        self.M = {}

    def load_data(self, tenor):
        data_dir = './data/'
        fname = 'LIBOR_' + str(tenor) + 'm_' + self.curr + '.csv'
        fpath = os.path.join(data_dir, fname)
        return pd.read_csv(fpath, header=0, names=['date', 'ir'])[::-1] 
        
    def prepare_data(self, df):
        #Trim the data to include only the time interval requested.
        if self.t_ival is not None:
            cond = ((df['date'] >= self.t_ival[0]) & (df['date'] <= self.t_ival[1]))
            df = df[cond]
        #Some rows have a dot as entries for the intrabank rate. Romore these.
        df = df[df['ir'].map(lambda x: str(x)!='.')]         
        #Change type of the ir column to numeric.
        df['ir'] = pd.to_numeric(df['ir'])
        return df

    def remove_spikes(self, df, key):
        window = 17
        ir = df[key].values
        ir_smooth = savgol_filter(ir, window, 3)
        std = pd.Series(ir).rolling(window).std()
        std[0:window] = 0. #always keep the elements with incomplete windows.
        cond = (abs(ir) < abs(ir_smooth) + 3.*std)
        df = df[cond.values]
        return df

    def transform_data(self, df, incr):
        #Transform before computing increments.
        if self.application == 'simple_diff':
            df['ir_transf'] = df['ir'].diff(incr)
        elif self.application == 'log_ratio':
            df['ir_transf'] = np.log(df.ir / df.ir.shift(incr))
        else:
            raise ValueError(
              'Application %s is not supported' %self.application)
        #Do not include N (incr) first rows, they're NaN after transformation.
        df = df.iloc[incr:]
        return df

    def run(self):
        for tenor in self.tenor:
            for incr in self.incr:
                key = '{}m_{}d'.format(str(tenor), str(incr))
                df = self.load_data(tenor)
                df = self.prepare_data(df)
                df = self.remove_spikes(df, 'ir')
                df = self.transform_data(df, incr)
                df = self.remove_spikes(df, 'ir_transf')
                self.M[key] = df
        self.M['incr'] = self.incr
        self.M['tenor'] = self.tenor
        return self.M
