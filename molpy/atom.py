# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

from .base import Model
import numpy as np

class Atom(Model):
    
    def __init__(self, fields=None, copy=None, **data):
        super().__init__(1, fields, copy, **data)
