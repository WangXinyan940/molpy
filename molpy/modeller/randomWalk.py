# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-05-19
# version: 0.0.1

from molpy_cpp.randomWalk import SimpleRW as SimpleRW_cpp
import numpy as np

class randomWalk:
    
    def getLinearTopo(self, nsteps, offset=0):
        
        bondi = np.arange(nsteps)
        bondj = bondi + 1
        bonds = np.vstack((bondi, bondj)).T
        return bonds + offset
    
    def getGraftTopo(self, graft_idx, main_chain_length):
        
        return np.vstack((graft_idx, np.arange(len(graft_idx))+main_chain_length)).T

class SimpleRW(randomWalk):
    
    def __init__(self, box):
        
        if isinstance(box, (int, float)):
            _box = (0, box)
        
        self._workload = SimpleRW_cpp(*_box)
        
    def walkOnce(self, lchain, stepsize):
        
        return self._workload.walkOnce(lchain, stepsize)
    
    def walkOnceFrom(self, start, lchain, stepsize):
        
        return self._workload.walkOnceFrom(start, lchain, stepsize)
            
    def findStart(self):
        
        return self._workload.findStart()
