# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

from logging import warning
from typing import List, Literal, Optional
from molpy.bond import Bond
from molpy.angle import Angle
from molpy.dihedral import Dihedral
from molpy.neighborlist import NeighborList
from molpy.utils import fromStructToDict
from .topo import Topo
from .model import Model
from .atom import Atom
import numpy as np

class Atoms(Model):
    
    def __init__(self, fields:dict=None):
        super().__init__(fields)
        self.topo = Topo()
        
    @staticmethod
    def fromAtoms(atoms):
        return Atoms(atoms.fields)
    
    @staticmethod
    def fromDict(atomFields, topoFields):
        
        atoms = Atoms(atomFields)
        if 'topo' in topoFields:
            atoms.topo.setTopo(topoFields['topo'])
        
        if 'bondTypes' in topoFields:
            atoms.topo.setBondTypes(topoFields['bondTypes'])
        

        return atoms
        
    
    @property
    def atoms(self):
        return self.getAtoms()
    
    def getAtoms(self):
        atomList = []
        for i in range(self.natoms):
            atomInfo = {key:value[i] for key, value in self._fields.items()}
            atomList.append(Atom(atomInfo))
        return atomList    
    
    @property
    def natoms(self):
        return self.n
    
    def getAtomByIdx(self, idx):
        fields = {key:value[idx] for key, value in self._fields.items()}
        return Atom.fromAtom(fields)
    
    def groupby(self, field):
        
        struc = self.toStructuredArray()
        a = struc[struc[field].argsort()]
        groups = np.split(a, np.unique(a[field], return_index=True)[1][1:])
        atoms = []
        groups = [np.array(group, dtype=struc.dtype) for group in groups]
        for group in groups:
            atoms.append(Atoms(fromStructToDict(group)))
        return atoms

    @property
    def positions(self):
        if 'position' in self._fields:
            return self._fields['position']
        elif 'x' in self._fields and 'y' in self._fields and 'z' in self._fields:
            return self.mergeFields(['x', 'y', 'z'], 'position')
    
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
        
    def setTopo(self, connection):
        self.topo.setTopo(connection)
        
    def setPositions(self, positions, **kwargs):
        self._fields['position'] = positions

    def getBonds(self)->List[Bond]:
        bondIdx = self.topo.bonds
        if bondIdx is None:
            return []
        
        itoms = self.atoms[bondIdx[:, 0]]
        jtoms = self.atoms[bondIdx[:, 1]]
        bonds = [Bond(itom, jtom) for itom, jtom in zip(itoms, jtoms)]
        return bonds
    
    @property
    def nbonds(self)->int:
        return self.topo.nbonds
    
    def getBondIdx(self)->List[List]:
        return self.topo.bonds
    
    def getAngles(self)->List[Angle]:
        angleIdx = self.topo.angles
        if angleIdx is None:
            return []
        
        itoms = self.atoms[angleIdx[:, 0]]
        jtoms = self.atoms[angleIdx[:, 1]]
        ktoms = self.atoms[angleIdx[:, 2]]
        angles = [Angle(itom, jtom, ktom) for itom, jtom, ktom in zip(itoms, jtoms, ktoms)]
        return angles
    
    @property
    def nangles(self)->int:
        return self.topo.nangles
    
    def getAnglesIdx(self)->List[List]:
        return self.topo.angles
    
    def getDihedrals(self)->List[Dihedral]:
        
        dihedralIdx = self.topo.dihedrals
        if dihedralIdx is None:
            return []
        
        itoms = self.atoms[dihedralIdx[:, 0]]
        jtoms = self.atoms[dihedralIdx[:, 1]]
        ktoms = self.atoms[dihedralIdx[:, 2]] 
        ltoms = self.atoms[dihedralIdx[:, 3]]    
        dihedrals = [Dihedral(itom, jtom, ktom, ltom) for itom, jtom, ktom, ltom in zip(itoms, jtoms, ktoms, ltoms)]
        
        return dihedrals
    
    @property
    def ndihedrals(self)->int:
        return self.topo.ndihedrals
    
    def getDihedralIdx(self)->List[List]:
        return self.topo.dihedrals
    
    def append(self, atoms):
        
        if len(self._fields):
            # validation
            assert len(atoms._fields) == len(self._fields), ValueError(f'Number of fields in atoms ({len(atoms._fields)}) does not match number of fields in self ({len(self._fields)})')
        
        for key, value in atoms._fields.items():
            
            if self._fields.get(key, None) is not None:
                np.append(self._fields[key], value)
            else:
                self._fields[key] = value
        
        
class AtomManager:
    
    atomsTypes = [
        'Molecule'
    ]
    
    def __init__(self):
        
        self.reset()
        for atomsType in self.atomsTypes:
            setName = atomsType[0].lower() + atomsType[1:] + 's'
            setattr(self, setName, {})
        
    def reset(self):
        
        self.atoms = Atoms()
        
        for key in self.atomsTypes:
            setattr(self, key, {})
            
    def registerType(self, newType:str):
        
        setName = newType[0].lower() + newType[1:] + 's'
        
        if newType in self.atomsTypes:
            warning.warn(f'{newType} is already registered')
        
        else:
            self.atomsTypes.append(newType)
            setattr(self, f'{setName}', {})

    def append(self, atoms):
        
        self.atoms.append(atoms)