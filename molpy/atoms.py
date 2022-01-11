# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

from .topo import Topo
from .model import Model
from .atom import Atom
import numpy as np
from numpy.lib import recfunctions as rfn
        
class Atoms(Model):
    
    def __init__(self, natoms=None, data:dict=None, fromAtoms=None):
        super().__init__(natoms)
        self._topo = Topo()
        if data is not None:
            self._fields.update(data)
        if fromAtoms is not None:
            if isinstance(fromAtoms, Atoms):
                self._fields = fromAtoms._fields
            elif isinstance(fromAtoms, np.ndarray):
                for name in fromAtoms.dtype.names:
                    self._fields[name] = fromAtoms[name]
    
    @property
    def natoms(self):
        return self._n
    
    @property
    def atomInstances(self):
        return self.getAtoms()
    
    def __len__(self):
        return self._n
    
    def getAtomInstances(self):
        
        struc = self.toStructuredArray()
        atomList = np.zeros_like(struc, dtype=object)
        for i in range(len(struc)):
            atomList[i] = Atom(fromAtom=struc[i])
        return atomList


    def selectByFunc(self, func):
        """return selected atoms by the function. 

        Args:
            func (Callable): Select function. The function takes atoms.data as arg and must return a mask, which length equal to natoms.

        Returns:
            Atoms: subset of atoms
        """
        struc = self.toStructuredArray()
        mask = func(struc)
        newAtoms = struc[mask]
        atoms = Atoms(natoms=len(mask), fromAtoms=newAtoms)
        return atoms
    
    def groupby(self, field):
        
        struc = self.toStructuredArray()
        a = struc[struc[field].argsort()]
        groups = np.split(a, np.unique(a[field], return_index=True)[1][1:])
        atoms = []
        for group in groups:
            atoms.append(Atoms(natoms=len(group), fromAtoms=group))
        return atoms
        
    def loadTraj(self, traj):
        
        self._traj = traj

    @property
    def positions(self):
        if 'position' in self._fields:
            return self.data['position']
        elif 'x' in self._fields and 'y' in self._fields and 'z' in self._fields:
            return self.mergeFields(['x', 'y', 'z'], 'position')
        
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
        