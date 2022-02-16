# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

import numpy as np
from pathlib import Path

def shallowCopyArray(array):

    outter_shape = array.shape[0]
    tmp = np.zeros(outter_shape, dtype=object)
    for i in range(outter_shape):
        tmp[i] = array[i]
    return tmp    


class PathUtils:
    
    def __init__(self, rootPath=None):
        
        if rootPath:
            self.rootPath = Path(rootPath)
        else:
            self.rootPath = Path.cwd()
    
    def findAll(self, pattern, subDir=None, recursion=False):
        
        if subDir is not None:
            dir = Path.joinpath(self.rootPath, pattern)  # equal to self.rootPath / pattern
            if not dir.exists() and not dir.is_dir:
                raise LookupError(f'Not such directory: {dir}')
            
        if recursion:
            paths = dir.glob('**/'+pattern)
        else:
            paths = dir.glob(pattern)
            
        return list(paths)
    
    def exists(self, pattern, subDir=None, recursion=False):
        pass
