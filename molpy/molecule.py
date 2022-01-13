# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-13
# version: 0.0.1

import numpy as np
from molpy.model import Model

class Molecule(Model):
    
    def __init__(self, n, data:dict=None, fromMolecule=None):
        super().__init__(n)