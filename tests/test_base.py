# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from molpy.base import Model
import numpy as np
import numpy.testing as npt
import pytest

class TestModel:
    
    @pytest.fixture(name='model')
    def test_init(self):
        
        model = Model(5, [('id', int), ('position', float, (3, ))], group=[1,2,3,4,5], vel=np.random.random((5, 3)))
        npt.assert_array_equal(model.data['id'], np.zeros(5))
        model.id = np.arange(5)
        npt.assert_array_equal(model.data['id'], np.arange(5))
        
        void_model = Model(1)
        assert void_model
        yield model
        
    def test_sync(self, model):
        data = model.data
        model.data['id'] = np.arange(5)
        npt.assert_array_equal(data, model.data)
        assert data[-1]['id'] == 4
        
        d0 = model.data[0]
        assert d0['id'] == 0
        model.data['id'] = np.arange(5)+1
        npt.assert_array_equal(model.data['id'], np.arange(5)+1)
        assert d0['id'] == 1