# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

import numpy as np
from molpy.atom import Atom


class Dihedral:
    
    def __init__(self, itom, jtom, ktom, ltom) -> None:
        pass

class Dihedrals:
    
    def __init__(self, dihedrals, atoms) -> None:
        self.dihedralIdx = Dihedrals.unique(dihedrals)
        self.atoms = atoms
        
    @staticmethod
    def unique(dihedrals):
        dihedrals = np.array(dihedrals)
        dihedrals = np.where((dihedrals[:,1]>dihedrals[:,2]).reshape((-1, 1)), dihedrals[:, ::-1], dihedrals)
        return np.unique(dihedrals, axis=0)
        
    @property
    def ndihedrals(self):
        return len(self.dihedralIdx)
    
    def __len__(self):
        return len(self.dihedralIdx)
    
    def getDihedralInstances(self):
        
        if self.atoms is None:
            raise ValueError(f'need atoms to generate Angle instances')
        
        itoms = self.atoms[self.dihedralIdx[:, 0]]
        jtoms = self.atoms[self.dihedralIdx[:, 1]]
        ktoms = self.atoms[self.dihedralIdx[:, 2]]
        ltoms = self.atoms[self.dihedralIdx[:, 3]]
        
        dihes = [Dihedrals(itom, jtom, ktom, ltom) for itom, jtom, ktom, ltom in zip(itoms, jtoms, ktoms, ltoms)]
        return dihes