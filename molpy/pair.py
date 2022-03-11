# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-08
# version: 0.0.1

import numpy as np


class Pair:
    
    def __init__(self, itom, jtom, distance=None):
        
        self.itom = itom
        self.jtom = jtom
        self._distance = distance
        
    @property
    def distance(self):
        if self._distance is None:
            return self.getDistance()
        else:
            return self._distance
        
    def getDistance(self):
        
        self._distance = np.linalg.norm(self.itom.position - self.jtom.position)
        return self._distance
    
    