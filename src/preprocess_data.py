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
        df['date'] = pd.to_datetime(df['date'])
        #Trim the data to include only the time interval requested.
        if self.t_ival is not None:
            cond = ((df['date'] >= self.t_ival[0]) & (df['date'] <= self.t_ival[1]))
            df = df[cond]
        #Some rows have a dot as entries for the intrabank rate. Romore these.
        df = df[df['ir'].map(lambda x: str(x)!='.')]         
        #Change type of the ir column to numeric.
        df['ir'] = pd.to_numeric(df['ir'])
        return df

    def remove_spikes(self, df):
        #Smooth the data and compute a rolling standard deviation day-wise
        #using 5 days windows.
        ir = df['ir'].values
        dates = df['date'].values
        ir_smooth = savgol_filter(ir, 9, 3)
        hw = pd.Timedelta(4., 'D') #date half window.
        sd = []
        for i,d in enumerate(dates):
            cond = ((df['date'] >= d - hw) & (df['date'] <= d + hw))
            diff = df['ir'][cond].values - ir_smooth[cond]
            sd.append(np.sqrt(np.sum(np.power(diff, 2))))
        df = df[(df['ir'] - ir_smooth).abs() < 5*np.array(sd)]
        return df

    def transform_data(self, df):
        if self.application == 'simple_diff':
            df['ir_transf'] = df['ir'].diff(1)
        elif self.application == 'log_ratio':
            df['ir_transf'] = np.log10(df.ir / df.ir.shift())
        else:
            raise ValueError(
              'Application %s is not supported' %self.application)
        return df

    def average_over_increment(self, df, incr):
        #Do not include first row, it contains NaN after transformation.
        df = df.iloc[1:]
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
                #df = self.remove_spikes(df)
                df = self.transform_data(df)
                df = self.average_over_increment(df, incr)
                self.M[key] = df
        return self.M
