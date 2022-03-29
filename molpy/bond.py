# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-04
# version: 0.0.2

import numpy as np
from molpy.interaction import register

class Bond:
    
    def __init__(self, itom, jtom, type=None):
        self.itom = itom
        self.jtom = jtom
        self.type = type
        
    def getLength(self):
        
        return np.linalg.norm(self.itom.position - self.jtom.position)

    def setBondType(self, bondType):
        name = bondType.name
        bondStyle = register.getBondInteraction(name)
        b = bondStyle(**bondType.properties)
        self.getEnergy = b.getEnergy
        self.getForce = b.getForce
        
    def __getitem__(self, o):
        tmp = [self.itom, self.jtom]
        return tmp[o]
        
