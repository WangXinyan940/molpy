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

