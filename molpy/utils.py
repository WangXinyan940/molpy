# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

import numpy as np


def fromDictToStruct(d:dict):
    names = d.keys()
    values = d.values()
    dtypes = [v.dtype for v in values]
    maxLength = max(map(len, values))
    arr = np.empty((maxLength, ), dtype=np.dtype(list(zip(names, dtypes))))
    for k, v in zip(names, values):
        arr[k] = v
        
    return arr

def fromStructToDict(arr):
    return {k: arr[k] for k in arr.dtype.names}

