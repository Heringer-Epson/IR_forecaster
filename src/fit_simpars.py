#!/usr/bin/env python

import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

rstats = rpackages.importr('stats')
utils = rpackages.importr('utils')
base = rpackages.importr('base')
rpackages.importr("Sim.DiffProc")
utils.chooseCRANmirror(ind=1)

#References
#https://rpy2.readthedocs.io/en/version_2.8.x/introduction.html
#http://rpy.sourceforge.net/rpy2/doc-2.1/html/introduction.html
#https://cran.r-project.org/web/packages/Sim.DiffProc/vignettes/fitsde.html

#Requirement:
#rpy2 (see https://anaconda.org/r/rpy2)
#conda install -c r rpy2

class Fit_Simpars(object):
    """
    Description:
    ------------
    TBW.

    Parameters:
    -----------
    TBW.
    """        
    def __init__(self, X, model):
        self.X = X
        self.model = model
        
        self.fitter = None
        self.fit = None

    def install_R_packages(self):
        pkg = 'Sim.DiffProc'
        if not rpackages.isinstalled(pkg):
            utils.install_packages(StrVector(pkg))

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
                               start = list(theta1=-0.001, theta2=0.0, theta3=0.005),
                               pmle="kessler")
              sol = coef(fitmod)
              return(sol)
              }
              """
              )
 
        elif self.model == 'Brownian':
            robjects.r(
              """
              fit_data <- function(data) {
              fx <- expression( theta[1]*x )
              gx <- expression( theta[2]*x )
              fitmod <- fitsde(data = data, drift = fx, diffusion = gx,
                               start = list(theta1=0.005, theta2=0.005),
                               pmle="kessler")
              sol = coef(fitmod)
              return(sol)
              }
              """
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
        self.install_R_packages() #move this to an installation file.
        self.define_model()
        self.perform_fit()
        return self.fit
