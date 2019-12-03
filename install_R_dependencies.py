import rpy2
from rpy2.robjects.packages import importr
utils = importr('utils')

from rpy2.robjects.packages import importr
utils = importr('utils')
utils.install_packages('Sim.DiffProc', repos="http://cran.us.r-project.org")
rpackages.importr('Sim.DiffProc')
