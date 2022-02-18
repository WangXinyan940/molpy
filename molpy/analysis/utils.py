# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-02-17
# version: 0.0.1

import numpy as np


class Accumulator:
    
    def __init__(self, name, op, init_value=None) -> None:
        self._name = name
        self.data = init_value
        self.op = op
        
    def __call__(self, X, op=None):
        
        Xarr = np.array(X)
        if op is None:
            op = self.op
        
        if self.data is None:
            self.data = Xarr
        else:
            if op == 'add':
                self.data += Xarr
            elif op == 'mul':
                self.data *= Xarr
        
        return self.data