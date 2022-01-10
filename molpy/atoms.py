# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

from .topo import Topo
from .base import Model
from .atom import Atom
import numpy as np
from molpy.utils import shallowCopyArray
        
class Atoms(Model):
    
    def __init__(self, natoms, fields=None, copy=None, **data):
        super().__init__(natoms, fields, copy, **data)
        self._topo = Topo(self.data)
    
    @property
    def natoms(self):
        return self._size
    
    @property
    def atomInstances(self):
        return self.getAtoms()
    
    def getAtoms(self):
        return self.data
    
    def __len__(self):
        return self._size
    
    def getAtomInstances(self):
        
        return [Atom(copy=copy) for copy in self.data]
        # return [copy for copy in self.data]

    def selectByFunc(self, func, copy=False):
        
        mask = func(self.data)
        if copy:
            raise NotImplementedError
        else:
            newAtoms = self.data[mask]
        return newAtoms
    
    def selectByExpr(self, expression, copy=False):
        pass
        
    def loadTraj(self, traj):
        
        self._traj = traj
        
    def getFrame(self, frame):
        
        atomArr = self._traj.parse(frame)
        for name in atomArr.dtype.names:
            self.data[name] = atomArr[name]

    @property
    def positions(self):
        if 'position' in self.data.dtype.names:
            return self.data['position']
        else:
            return np.hstack([self.data['x'].reshape((self.natoms, 1)), self.data['y'].reshape((self.natoms, 1)), self.data['z'].reshape((self.natoms, 1))])
