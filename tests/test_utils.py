# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

import numpy as np
import numpy.testing as npt
import pytest
from molpy.utils import fromDictToStruct, fromStructToDict

class TestUtils:
    
    @pytest.fixture(scope='module', name='ref')
    def test_init(self):
        
        d = {'element': np.array(['H', 'H', 'H', 'H', 'H']),
             'mass': np.array([1.00782503207, 1.00782503207, 1.00782503207, 1.00782503207, 1.00782503207]),}
        
        dtypes = ['<U2', '<f8']
        
        arr = np.empty((5, ), dtype=np.dtype(list(zip(d.keys(), dtypes))))
        arr['element'] = d['element']
        arr['mass'] = d['mass']
        
        assert arr['element'][-1] == 'H'
        assert arr['mass'][-1] == 1.00782503207
        
        yield d, arr
        
    def test_fromDictToStruct(self, ref):
        
        d, arr = ref
        
        arr1 = fromDictToStruct(d)
        npt.assert_equal(arr1['element'], arr['element'])
        npt.assert_equal(arr1['mass'], arr['mass'])
        
    def test_fromStructToDict(self, ref):
        
        d, arr = ref
        
        d1 = fromStructToDict(arr)
        npt.assert_equal(d1['element'], d['element'])
        npt.assert_equal(d1['mass'], d['mass'])
