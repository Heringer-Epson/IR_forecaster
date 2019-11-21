#!/usr/bin/env python

import numpy as np
import pandas as pd

class Compute_Structure(object):
    """
    Description:
    ------------
    TBW.

    Parameters:
    -----------
    TBW.

    """        
    def __init__(self, merged_df):
        self.merged_df = merged_df
        
    def get_montly_avg(self):
        monthly_df = self.merged_df.resample('M').mean()
        return monthly_df.values

    def get_yearly_avg(self):
        yearly_df = self.merged_df.resample('Y').mean()
        yearly_std_df = self.merged_df.resample('Y').std()
        labels_yr = [date.year for date in yearly_df.index]
        return yearly_df.values, yearly_std_df.values, labels_yr
