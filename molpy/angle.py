# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

import numpy as np

from molpy.atom import Atom
from molpy.utils import shallowCopyArray
     
class Angle:
    
    def __init__(self, itom, jtom, ktom):
        self.itom = itom
        self.jtom = jtom
        self.ktom = ktom

class Angles:
    
    def __init__(self, angles, atoms=None):
        
        self.angles = Angles.unique(angles)
        self.atoms = atoms
        
    @staticmethod
    def unique(angles):
        angles = np.array(angles)
        angles = np.where((angles[:,0]>angles[:,2]).reshape((-1, 1)), angles[:, ::-1], angles)
        return np.unique(angles, axis=0)
    
    @property
    def nangles(self):
        return len(self.angles)
    
    def __len__(self):
        return len(self.angles)
    
    def getAngleInstances(self):
        
        if self.atoms is None:
            raise ValueError(f'need atoms to generate Angle instances')
    
        itoms = self.atoms[self.angles[:, 0]]
        jtoms = self.atoms[self.angles[:, 1]]
        ktoms = self.atoms[self.angles[:, 2]]
        
        angles = [Angle(itom, jtom, ktom) for itom, jtom, ktom in zip(itoms, jtoms, ktoms)]      
        return angles  