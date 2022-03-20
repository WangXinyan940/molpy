# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

from .model import Model

class Atom(Model):
    
    def __init__(self, fields:dict=None):
        super().__init__(fields)
        
    @staticmethod
    def fromAtom(atom):
        pass

    @property
    def x(self):
        return self.position[0]
    
    @property
    def y(self):
        return self.position[1]
    
    @property
    def z(self):
        return self.position[2]
