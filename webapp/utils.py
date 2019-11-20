import sys
import os
import operator
import numpy as np
import pandas as pd

#Conversors.
transf2application = {'Raw':'simple_diff', 'Increment':'simple_diff',
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
