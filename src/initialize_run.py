#!/usr/bin/env python

import os

class Init_Run(object):
    """
    TBW.
                    
    Outputs:
    --------
    None
    """    
    
    def __init__(self, curr, application):
        self.curr = curr
        self.application = application
        
        self.outdir = None
    
    def init_outdir(self):
        
        run_dir = self.curr + '_' + self.application
        self.outdir = os.path.join('./../OUTPUTS/RUNS/', run_dir)
        if not os.path.isdir(self.outdir):
            os.mkdir(self.outdir)
            os.mkdir(os.path.join(self.outdir, 'IR'))
            os.mkdir(os.path.join(self.outdir, 'distributions'))
        
    def run_init(self):
        self.init_outdir()
        return self.outdir
