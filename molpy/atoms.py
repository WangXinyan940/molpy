# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

from .topo import Topo
from .model import Model
from .atom import Atom
import numpy as np

class Atoms(Model):
    
    def __init__(self, natoms=None, data:dict=None, fromAtoms=None, connection=None):
        
        super().__init__(natoms)
        if data is not None:
            self._fields.update(data)
        if fromAtoms is not None:
            if isinstance(fromAtoms, Atoms):
                self._fields = fromAtoms._fields
            elif isinstance(fromAtoms, np.ndarray):
                for name in fromAtoms.dtype.names:
                    self._fields[name] = fromAtoms[name]
        
        # this must be the last one be initialize   
        self._topo = Topo(connection, self)
    
    @property
    def natoms(self):
        return self._n
    
    def __len__(self):
        return self._n
    
    def getAtoms(self):
        
        struc = self.toStructuredArray()
        atomList = np.zeros_like(struc, dtype=object)
        for i in range(len(struc)):
            atomList[i] = Atom(fromAtom=struc[i])
        return atomList

    atoms = property(getAtoms)

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
        pass
    
    def calcCenterOfMass(self):
        pass
    
    def getBondIdx(self):
        return self._topo.getBonds()
    
    def getAngleIdx(self):
        return self._topo.getAngles()
    
    def getDihedralIdx(self):
        return self._topo.getDihedrals()
    
    bonds = property(getBondIdx)
    angles = property(getAngleIdx)
    dihedrals = property(getDihedralIdx)