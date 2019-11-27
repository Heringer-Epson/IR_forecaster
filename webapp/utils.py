import sys
import os
import operator
import numpy as np
import pandas as pd
from datetime import datetime as dt

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from preprocess_data import Preproc_Data

#Conversors.
transf2application = {'Raw':'simple_diff', 'Diff.':'simple_diff',
                      'Log ratio':'log_ratio'}
transf2IR = {'Raw':'ir', 'Diff.':'ir_transf', 'Log ratio':'ir_transf'}
currtag2curr = {'USD':['USD'], 'CAD':['CAD'], 'USD & CAD':['USD', 'CAD']}
incrtag2incr = {'1':[1], '25':[25], '1 & 25':[1, 25]}

pars2guess = {
  'Raw_Vasicek': 'theta1=0.1, theta2=0.1, theta3=0.05',
  'Diff._Vasicek': 'theta1=0.0001, theta2=1., theta3=0.005',
  'Log ratio_Vasicek': 'theta1=0.0001, theta2=1., theta3=0.005',
  'Raw_Brownian': 'theta1=0.005, theta2=0.005',
  'Diff._Brownian': 'theta1=0.003, theta2=0.00001', ##Improve
  'Log ratio_Brownian': 'theta1=0.005, theta2=0.005' ##Improve
}

def sort_pdfs(D, pdfs):
    aux = {}
    for pdf in pdfs:
        aux[pdf] = D['D_' + pdf]
    sorted_aux = sorted(aux.items(), key=operator.itemgetter(1))
    pdf_sorted_list = [entry[0] for entry in sorted_aux]
    return pdf_sorted_list

def make_fit_df(D, pdfs):
    p_col = [D['p_' + pdf] for pdf in pdfs]
    D_col = [D['D_' + pdf] for pdf in pdfs]
    return pd.DataFrame({'Distribution':pdfs, 'D':D_col, 'p':p_col})

def format_date(time_range):
    t_min = '{:04d}-{:02d}-01'.format(int(time_range[0] // 1),
                                      int(12.*(time_range[0] % 1)) + 1)
    t_max = '{:04d}-{:02d}-01'.format(int(time_range[1] // 1),
                                      int(12.*(time_range[1] % 1)) + 1)
    return t_min, t_max

def merge_dataframes(list_M, list_curr, list_tenor, list_incr, qtty):
    list_df = []
    for M, curr in zip(list_M,list_curr):
        for incr in list_incr:
            for t in list_tenor:
                key = '{}m_{}d'.format(str(t),str(incr))
                aux = M[key][['date',qtty]]
                aux.set_index('date', inplace=True)
                aux.rename(columns={
                  qtty:qtty + '_{}_{}m'.format(curr, str(t))}, inplace=True)
                list_df.append(aux)
    merged_df = pd.concat(list_df, axis=1, join='inner', ignore_index=False)
    merged_df.index = pd.to_datetime(merged_df.index)
    return merged_df

def make_transf_label(transf, incr=None):
    if incr is None:
        T = 'T'
    else:
        T = '{} day'.format(str(incr))
    if transf == 'Diff.':
        label = r'IR(Date + {}) - IR(Date)'.format(T)
    elif transf == 'Log ratio':
        label = r'ln (IR(Date + {}) / IR(Date))'.format(T)
    elif transf == 'Raw':
        label = r'IR(Date)'.format(T)    
    return label
    
def compute_t_range(currtag='USD', incrtag='1', tenor=[1,2,3,6,12]):
       
    list_t_min, list_t_max = [], []

    curr_list = currtag2curr[currtag]
    incr_list = incrtag2incr[incrtag]    
    for curr in curr_list:
        M = Preproc_Data(curr=curr, incr=incr_list).run()
        for incr in incr_list:
            for t in tenor:
                key = '{}m_{}d'.format(str(t),str(incr))
                dates = M[key]['date'].values
                list_t_min.append(min(dates))
                list_t_max.append(max(dates))
    
    t_min = dt.strptime(max(list_t_min), '%Y-%m-%d')
    t_max = dt.strptime(min(list_t_max), '%Y-%m-%d')
    #Don't use data prior to 1990.
    t_min = max([t_min, dt.strptime('1990-01-01', '%Y-%m-%d')])
    
    t_min = t_min.year + (t_min.month - 1.) / 12.
    t_max = t_max.year + (t_max.month - 1.) / 12.

    t_list = [int(t) for t in np.arange(t_min,t_max + 0.0001,1)]
    return t_min, t_max, t_list
