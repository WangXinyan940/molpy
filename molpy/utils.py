# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

import numpy as np

def shallowCopyArray(array):

    outter_shape = array.shape[0]
    tmp = np.zeros(outter_shape, dtype=object)
    for i in range(outter_shape):
        tmp[i] = array[i]
    return tmp    
