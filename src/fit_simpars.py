#!/usr/bin/env python

import os
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

rstats = rpackages.importr('stats')
utils = rpackages.importr('utils')

R_cloud_path = '/usr/local/lib/R/site-library'
if os.path.isdir(R_cloud_path):
    rpackages.importr('Sim.DiffProc', lib_loc=R_cloud_path )
else:
    rpackages.importr('Sim.DiffProc')

class Fit_Simpars(object):
    """
    Description:
    ------------
    Computes the best fit parameters for a given choice of stochastic
    differential equation (sde).

    Parameters:
    -----------
    X : ~np.array
        Array to be fitted. It contains IR (or transformed IR) data.
    model : ~str
        Which financial model to be fitted. Currently accepts:
            'Brownian', for the geometric brownian model.
            'Vasicek', for the Vasicel (a.k.a. Ornstein–Uhlenbeck) model.
    guess : ~str
        A string containing the initial guess parameters for the taget model.
    
    Notes:
    ------
    Requires the 'Sim.DiffProc' R package to have been previously installed.

    Return:
    -------
    fit: A list containing the best fit parameters.
    """        
    def __init__(self, X, model, guess):
        self.X = X
        self.model = model
        self.guess = guess
        
        self.fitter = None
        self.fit = None

    def define_model(self):
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
        #Whereas the geomatric brownian model states that:
        #(see https://en.wikipedia.org/wiki/Geometric_Brownian_motion)
        #dX_t = mu*X_t*dt + sigma*X_t*dW_t
        
        if self.model == 'Vasicek':
            robjects.r(
              """
              fit_data <- function(data) {
              fx <- expression( theta[1]*(theta[2] - x) )
              gx <- expression( theta[3] )
              fitmod <- fitsde(data = data, drift = fx, diffusion = gx,
                               start = list(%s),
                               pmle="euler", lower=c(-Inf,0,0))
              sol = coef(fitmod)
              return(sol)
              }
              """ %(self.guess)
              )
 
        elif self.model == 'Brownian':
            robjects.r(
              """
              fit_data <- function(data) {
              fx <- expression( theta[1]*x )
              gx <- expression( theta[2]*x )
              fitmod <- fitsde(data = data, drift = fx, diffusion = gx,
                               start = list(%s),
                               pmle="euler", lower=c(-Inf,0))
              sol = coef(fitmod)
              return(sol)
              }
              """ %(self.guess)
              )

        else:
            raise valueError('Requested model is not available.')
        
        self.fitter = robjects.r['fit_data']
          
    def perform_fit(self):
        dt = 1./253. #Work days. (In units of years).
        X_R = rstats.ts(robjects.FloatVector(self.X), deltat=dt)
        sol = self.fitter(X_R)
        self.fit = [sol[i] for i in range(len(sol))]

    def run(self):
        self.define_model()
        self.perform_fit()
        return self.fit
