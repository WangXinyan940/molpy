# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

from .topo import Topo
from .base import Model
from .atom import Atom
import numpy as np
from numpy.lib import recfunctions as rfn
        
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

    def selectByFunc(self, func):
        """return selected atoms by the function. 

        Args:
            func (Callable): Select function. The function takes atoms.data as arg and must return a mask, which length equal to natoms.

        Returns:
            Atoms: subset of atoms
        """
        mask = func(self.data)
        newAtoms = self.data[mask]
        atoms = Atoms(copy=newAtoms)
        return atoms
    
    def selectByExpr(self, expression, copy=False):
        
        return Atoms(copy=self.data[exec(expression)])
        
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

    def mergeAtoms(self, atoms):
        """merge anthoer atoms to this one

        Args:
            atoms ([type]): [description]
        """
        # untest
        self.data = rfn.merge_arrays([self.data, atoms.data])
        
    def mergeFields(self, newdtype):
        
        self._data = rfn.unstructured_to_structured(rfn.structured_to_unstructured(self.data), newdtype)
        
    def dropFields(self, fields):
        self._data = rfn.drop_fields(self._data, fields)
        
    def calcRadiusOfGyration(self):
        
        # def radgyr(atomgroup, masses, total_mass=None):
        if 'mass' in self.data.dtype.names:
            masses = self.data['mass']
        else:
            masses = np.ones(len(self.natoms))
        # coordinates change for each frame
        coordinates = self.positions
        center_of_mass = self.center_of_mass()

        # get squared distance from center
        ri_sq = (coordinates-center_of_mass)**2
        # sum the unweighted positions
        sq = np.sum(ri_sq, axis=1)
        sq_x = np.sum(ri_sq[:,[1,2]], axis=1) # sum over y and z
        sq_y = np.sum(ri_sq[:,[0,2]], axis=1) # sum over x and z
        sq_z = np.sum(ri_sq[:,[0,1]], axis=1) # sum over x and y

        # make into array
        sq_rs = np.array([sq, sq_x, sq_y, sq_z])

        # weight positions
        rog_sq = np.sum(masses*sq_rs, axis=1)/np.sum(masses)
        # square root and return
        return np.sqrt(rog_sq)
    
    def calcCenterOfMass(self):
        if 'mass' in self.data.dtype.names:
            masses = self.data['mass']
        else:
            masses = np.ones(len(self.natoms))
        cm = self.positions * masses[:, None]
        cm = np.sum(cm, axis=0) / len(cm) / np.sum(masses)
        return cm
        