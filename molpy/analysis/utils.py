# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-02-17
# version: 0.0.1

from typing import Iterable
import numpy as np
from functools import partial, reduce

class Accumulator:
    
    def __init__(self, op, name, init_value=None):
        self.name = name
        self.op = op
        self.value = init_value
        
    def __call__(self, X, op=None):
        
        if self.value is None:
            self.value = X
            return self
        
        else:
            if op is None:
                p_op = partial(self.op, self.value)
            else:
                p_op = partial(op, self.value)
                
            self.value = p_op(X)
            return self

    def __repr__(self) -> str:
        return f'< Accumulator {self.name} >'
    
class Reducer:
    
    def __init__(self, op, name, init_value=None) :
        
        self.name = name 
        self.op = op
        self.value = init_value
        
    def __call__(self, X:Iterable):
        iterator = iter(X)
        if self.value is None:
            self.value = next(iterator)
        
        op = self.op
        self.value = reduce(op, iterator, self.value)
        return self
    
    def __repr__(self) -> str:
        return f' < Reducer {self.name} > '
            