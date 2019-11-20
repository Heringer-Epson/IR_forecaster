#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter 

class Preproc_Data(object):
    """
    This class contains methods to read and preprocess the data. Preprocessing
    includes removing spikes and smoothing the data.
                
    RETURN:
    -------
    A dataframe with the following columns:
      $date: array of np.datetime64 times.
      $ir: intrabank interest rate
    """    
    
    def __init__(self, curr, t_ival, application, tenor, incr):
        self.curr = curr
        self.t_ival = t_ival
        self.application = application
        self.tenor = tenor
        self.incr = incr
        self.M = {}
        self.df = None

    def load_data(self, tenor):
        data_dir = './../data/'
        fname = 'LIBOR_' + str(tenor) + 'm_' + self.curr + '.csv'
        fpath = os.path.join(data_dir, fname)
        return pd.read_csv(fpath, header=0, names=['date', 'ir'])[::-1] 
        
    def prepare_data(self, df):
        #Convert date column type to a datetime object.
        #df['date'] = [pd.to_datetime(df['date'])]
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
        window = 9
        ir = df['ir'].values
        ir_smooth = savgol_filter(ir, window, 3)
        std = pd.Series(ir).rolling(window).std()
        std[0:window] = 0. #always keep the elements with incomplete windows.
        cond = (ir < ir_smooth + 3.*std)
        df = df[cond.values]
        return df

    def transform_data(self, df):
        if self.application == 'simple_diff':
            df['ir_transf'] = df['ir'].diff(1)
        elif self.application == 'log_ratio':
            df['ir_transf'] = np.log10(df.ir / df.ir.shift())
        else:
            raise ValueError(
              'Application %s is not supported' %self.application)
        #Do not include first row, it contains NaN after transformation.
        df = df.iloc[1:]
        return df

    def average_over_increment(self, df, incr):
        group_index = np.arange(len(df))//incr
        aggregator = {'date':['first', 'last'], 'ir':[np.mean, np.std],
                      'ir_transf':[np.mean, np.std]}
        #Compute averaged quantities and rename columns to reflect that.
        df = df.groupby(group_index).agg(aggregator)
        df.columns = [
          'last_date', 'first_date', 'ir_mean', 'ir_std', 'ir_transf_mean',
          'ir_transf_std']
        df.reindex(columns=sorted(df.columns))
        return df

    def run_preproc_data(self):
        for tenor in self.tenor:
            for incr in self.incr:
                key = '{}m_{}d'.format(str(tenor), str(incr))
                df = self.load_data(tenor)
                df = self.prepare_data(df)
                df = self.remove_spikes(df, 'ir')
                df = self.transform_data(df)
                df = self.remove_spikes(df, 'ir_transf')
                df = self.average_over_increment(df, incr)
                self.M[key] = df
        return self.M
