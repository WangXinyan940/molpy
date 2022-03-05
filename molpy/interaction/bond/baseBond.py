# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-05
# version: 0.0.1

import numpy as np

class BaseBond:

    def __init__(self, itom, jtom):
        self.itom = itom
        self.jtom = jtom

    def getEnergy(self, r):
        raise NotImplementedError
    
    def getForce(self, r):
        raise NotImplementedError
    
    def getLength(self):
        
        return np.linalg.norm(self.itom.position - self.jtom.position)
    
