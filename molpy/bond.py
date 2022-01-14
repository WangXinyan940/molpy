# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-04
# version: 0.0.2

import numpy as np

from molpy.atom import Atom
from molpy.utils import shallowCopyArray

class Bond:
    
    def __init__(self, itom, jtom):
        self.itom = itom
        self.jtom = jtom

class Bonds:
    
    def __init__(self, bonds, atoms=None) -> None:
        
        self.bondIdx = Bonds.unique(bonds)
        self.atoms = atoms
    
    @staticmethod 
    def unique(bonds):
        bonds = np.array(bonds)
        bonds = np.sort(bonds, axis=1)
        bonds = np.unique(bonds, axis=0)
        return bonds
        
    @property
    def nbonds(self):
        return len(self.bondIdx)
    
    def __len__(self):
        return len(self.bondIdx)
    
    def getBondInstances(self):
        
        if self.atoms is None:
            raise ValueError
        
        itoms = self.atoms[self.bondIdx[:, 0]]
        jtoms = self.atoms[self.bondIdx[:, 1]]

        bonds = [Bond(atom, btom) for atom, btom in zip(itoms, jtoms)]
        return bonds

