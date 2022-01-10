# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

import numpy as np
from molpy.atom import Atom
from molpy.utils import shallowCopyArray

class Dihedral:
    
    def __init__(self, itom, jtom, ktom, ltom) -> None:
        pass

class Dihedrals:
    
    def __init__(self, dihedrals, atoms) -> None:
        self.dihedrals = Dihedrals.unique(dihedrals)
        self.atoms = atoms
        
    @staticmethod
    def unique(dihedrals):
        dihedrals = np.array(dihedrals)
        dihedrals = np.where((dihedrals[:,1]>dihedrals[:,2]).reshape((-1, 1)), dihedrals[:, ::-1], dihedrals)
        return np.unique(dihedrals, axis=0)
        
    @property
    def ndihedrals(self):
        return len(self.dihedrals)
    
    def __len__(self):
        return len(self.dihedrals)
    
    def getDihedralInstances(self):
        
        if self.atoms is None:
            raise ValueError(f'need atoms to generate Angle instances')
        
        tmp = shallowCopyArray(self.atoms)

        itoms = map(lambda copy: Atom(copy=copy), tmp[self.dihedrals[:, 0]])
        jtoms = map(lambda copy: Atom(copy=copy), tmp[self.dihedrals[:, 1]])
        ktoms = map(lambda copy: Atom(copy=copy), tmp[self.dihedrals[:, 2]])
        ltoms = map(lambda copy: Atom(copy=copy), tmp[self.dihedrals[:, 2]])
        
        dihes = [Dihedrals(itom, jtom, ktom, ltom) for itom, jtom, ktom, ltom in zip(itoms, jtoms, ktoms, ltoms)]
        return dihes