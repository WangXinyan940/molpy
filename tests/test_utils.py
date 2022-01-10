# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

import numpy as np
import numpy.testing as npt

from molpy.utils import shallowCopyArray

class TestUtils:
    
    def test_shallowCopyArray(self):
        
        arr1d = np.arange(5)
        copy = arr1d[:3]
        arr1d[:] = np.zeros_like(arr1d)
        npt.assert_array_equal(copy, arr1d[:3])
        
        copy = arr1d[::2]
        arr1d[:] = np.ones_like(arr1d)
        npt.assert_array_equal(copy, arr1d[::2])
        
        copy = arr1d[[0, 2]]
        arr1d[:] = np.zeros_like(arr1d)
        with npt.assert_raises(AssertionError):
            npt.assert_array_equal(copy, arr1d[[0, 2]])
        
        
        arr2d = np.ones((5, 3))
        copy = arr2d[:3]
        arr2d[:] = np.zeros_like(arr2d)
        npt.assert_array_equal(copy, arr2d[:3])
        
        copy = arr2d[::2]
        arr2d[:] = np.ones_like(arr2d)
        npt.assert_array_equal(copy, arr2d[::2])
        
        copy = arr2d[[0, 2]]
        arr2d[:] = np.zeros_like(arr2d)
        with npt.assert_raises(AssertionError):
            npt.assert_array_equal(copy, arr2d[[0, 2]])
            
            
        struc = np.zeros((5), dtype=[('name', str), ('position', float, 3)])
        copy = struc[:3]
        struc['name'] = [f'{i}' for i in range(5)]
        struc['position'] = np.random.random((5, 3))
        npt.assert_equal(copy, struc[:3])
        
        copy = struc[::2]
        struc['name'] = [f'-{i}' for i in range(5)]
        struc['position'] = np.random.random((5, 3))
        npt.assert_equal(copy, struc[::2])
        
        copy = struc[[0, 2]]
        struc['name'] = [f'{i}' for i in range(5)]
        struc['position'] = np.random.random((5, 3))
        with npt.assert_raises(AssertionError):
            npt.assert_equal(copy, struc[[0, 2]])
            
        """ 
        test shallowCopyArray
        def shallowCopyArray(array):

            outter_shape = array.shape[:-1]
            tmp = np.zeros(outter_shape, dtype=object)
            for i in range(outter_shape):
                tmp[i] = array[i]
            return tmp            
        """
        tmp = shallowCopyArray(arr1d)
        copy = tmp[[0, 2]]
        arr1d[:] = np.zeros_like(arr1d)
        npt.assert_array_equal(copy, arr1d[[0, 2]])
        
        arr2d = shallowCopyArray(arr2d)
        copy = arr2d[[0, 2]]
        arr2d[:] = np.zeros_like(arr2d)
        npt.assert_array_equal(copy[0], arr2d[0])
        
        tmp = shallowCopyArray(struc)
        copy = tmp[[0, 2]]
        struc['name'] = [f'{i}' for i in range(5)]
        struc['position'] = np.random.random((5, 3))
        npt.assert_equal(copy[0], struc[0])        
        npt.assert_equal(copy[1], struc[2])        