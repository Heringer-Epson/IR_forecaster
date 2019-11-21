import sys
import os
import operator
import numpy as np
import pandas as pd

#Conversors.
transf2application = {'Raw':'simple_diff', 'Diff.':'simple_diff',
                      'Log ratio':'log_ratio'}

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
    #return pd.DataFrame({'p':p_col, 'D':D_col}, index=pdfs)
    return pd.DataFrame({'Distribution':pdfs, 'D':D_col, 'p':p_col})

def format_date(time_range):
    t_min = '{:04d}-{:02d}-01'.format(int(time_range[0] // 1),
                                      int(12.*(time_range[0] % 1)) + 1)
    t_max = '{:04d}-{:02d}-01'.format(int(time_range[1] // 1),
                                      int(12.*(time_range[1] % 1)) + 1)
    return t_min, t_max

def merge_dataframes(M, tenor, incr, qtty):
    list_df = []
    for t in tenor:
        key = '{}m_{}d'.format(str(t),str(incr))
        aux = M[key][['date',qtty]]
        aux.set_index('date', inplace=True)
        aux.rename(columns={qtty:qtty + '_{}m'.format(str(t))}, inplace=True)
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
