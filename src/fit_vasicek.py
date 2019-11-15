#!/usr/bin/env python

import os
import numpy as np
import pandas as pd

import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
from rpy2.robjects.packages import importr

rstats = rpackages.importr('stats')
utils = rpackages.importr('utils')
base = rpackages.importr('base')
utils.chooseCRANmirror(ind=1)

importr("Sim.DiffProc")

#References
#https://rpy2.readthedocs.io/en/version_2.8.x/introduction.html
#http://rpy.sourceforge.net/rpy2/doc-2.1/html/introduction.html
#https://cran.r-project.org/web/packages/Sim.DiffProc/vignettes/fitsde.html

#Requirement:
#rpy2 (see https://anaconda.org/r/rpy2)
#conda install -c r rpy2

class Fit_Vasicek(object):
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
    def __init__(self, M, tenor, incr, outdir):
        self.M = M
        self.tenor = tenor
        self.incr = incr
        self.outdir = outdir
        
        self.fitter = None
        self.fits = {}

    def install_R_packages(self):
        pkg = 'Sim.DiffProc'
        if not rpackages.isinstalled(pkg):
            utils.install_packages(StrVector(pkg))

    def define_Vasicek_model(self):
        #E.g. https://cran.r-project.org/web/packages/Sim.DiffProc/vignettes/fitsde.html
        #Expression: dX_t = (theta_1 + theta_2*X_t)*dt [drift term]
        #                 + (theta_3 * X_t**theta_4*dW_t) [diffusion term]
        #Translates to the following expression in the code snipet below:
        #fx <- expression( theta[1]+theta[2]*x )
        #gx <- expression( theta[3]*x^theta[4] )
        #
        #The Vasicek model states that:
        #(see https://en.wikipedia.org/wiki/Vasicek_model)
        #
        #dX_t = a*(b - X_t)*dt + sigma*dW_t
        #Hence:
        #fx <- expression( theta[1]*(theta[2] - x) )
        #gx <- expression( theta[3] )
        
        robjects.r(
          """
          fit_data <- function(data) {
          fx <- expression( theta[1]*(theta[2] - x) )
          gx <- expression( theta[3] )
          fitmod <- fitsde(data = data, drift = fx, diffusion = gx,
                           start = list(theta1=1, theta2=1, theta3=1),
                           pmle="euler")
          sol = coef(fitmod)
          return(sol)
          }
          """
          )
        self.fitter = robjects.r['fit_data']
          
    def perform_fit(self):
        for incr in self.incr:
            for tenor in self.tenor:
                key = '{}m_{}d'.format(str(tenor), str(incr))
                X = self.M[key]['ir_transf_mean'].values
                dt = 1./365.*incr
                X_R = rstats.ts(robjects.FloatVector(X), deltat=dt)
                sol = self.fitter(X_R)
                self.fits[key] = [sol[i] for i in range(len(sol))]

    def make_fit(self):
        self.install_R_packages()
        self.define_Vasicek_model()
        self.perform_fit()
        return(self.fits)
