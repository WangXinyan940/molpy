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
            return self._fields['position']
        elif 'x' in self._fields and 'y' in self._fields and 'z' in self._fields:
            return self.mergeFields(['x', 'y', 'z'], 'position')
        
    def calcRadiusOfGyration(self):
        pass
    
    def calcCenterOfMass(self):
        pass
    
    def getBonds(self):
        return self._topo.bonds
    
    def getBondIdx(self):
        return self._topo.bondIdx
    
    def getAngles(self):
        return self._topo.angles
    
    def getAngleIdx(self):
        return self._topo.angleIdx
    
    def getDihedrals(self):
        return self._topo.dihedrals
    
    def getDihedralIdx(self):
        return self._topo.dihedralIdx
    
    bonds = property(getBonds)
    angles = property(getAngles)
    dihedrals = property(getDihedrals)
    bondIdx = property(getBondIdx)
    angleIdx = property(getAngleIdx)
    dihedralIdx = property(getDihedralIdx)
    
    @property
    def masses(self):
        if 'mass' in self._fields or 'masses' in self._fields:
            mass = self._fields['mass']
        else:
            mass = np.ones((len(self.positions)))
        return mass        
    
    def calcCenterOfMass(self):
        
        positions = self.positions
        mass = self.masses
        assert len(mass) == len(positions), ValueError
        return np.sum(positions * mass[:, None], axis=0)/self.natoms

    def calcRadiusOfGyration(self, mode='vector'):
        
        positions = self.positions
        mass = self.masses
        COM = self.calcCenterOfMass()
        
        # # get squared distance from center
        ri_sq = (positions-COM)**2
        # sum the unweighted positions
        sq = np.sum(ri_sq, axis=1)
        sq_x = np.sum(ri_sq[:,[1,2]], axis=1) # sum over y and z
        sq_y = np.sum(ri_sq[:,[0,2]], axis=1) # sum over x and z
        sq_z = np.sum(ri_sq[:,[0,1]], axis=1) # sum over x and y

        # make into array
        sq_rs = np.array([sq, sq_x, sq_y, sq_z])

        # weight positions
        rog_sq = np.sum(mass*sq_rs, axis=1)/np.sum(mass)
        # square root and return
        if mode == 'vector':
            return np.sqrt(rog_sq[0])