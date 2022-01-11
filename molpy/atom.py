# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

from .model import Model
import numpy as np

class Atom(Model):
    
    def __init__(self, data:dict=None, fromAtom=None):
        super().__init__(1, )
        if data is not None:
            self._fields.update(data)
        if fromAtom is not None:
            if isinstance(fromAtom, Atom):
                self._fields = fromAtom._fields
            elif hasattr(fromAtom, 'dtype'):
                for name in fromAtom.dtype.names:
                    self._fields[name] = fromAtom[name]       
