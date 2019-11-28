#!/usr/bin/env python

class Compute_Structure(object):
    """
    Description:
    ------------
    Given a dataframe of IR (or transformed IR) values according to each tenor,
    compute monthly and yearly averaged yields (term structure).

    Parameters:
    -----------
    merged_df : ~pandas dataframe
        Dataframe of IR (or transformed IR) values. Different columns contain
        data for each tenor.

    Return:
    -------
    monthly_df.values: a matrix containing the IRs averaged monthly.
    yearly_df.values: a matrix containing the IRs averaged yearly.
    yearly_std_df.values: The standard deviation for each mean computed above.
    labels_yr: the labels for the yearly averaged data.
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
