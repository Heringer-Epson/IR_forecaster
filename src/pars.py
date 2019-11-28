#!/usr/bin/env python

class Inp_Pars(object):
    """
    Description:
    ------------
    Contains parameters that are used in multiple routines.

    Parameters:
    -----------
    dt : ~float
        The time step to simulate future rates. In units of year
        where 1 business year ~ 253 days.
    T_sim : ~int
        Number of days to be simulated.
    MC_npaths : ~int
        Number of paths to be simulated.
    """        
    dt = 1./253. #Units of years (1 business year ~ 253 days).
    T_sim = 250
    MC_npaths = 100 
    def __init__(self):
        pass


