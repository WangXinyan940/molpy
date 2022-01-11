# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-11
# version: 0.0.2

# TODO: new model to replace structure array

import pytest
import numpy as np
import numpy.testing as npt
from molpy.model import Model

class TestModel:
    
    @pytest.fixture(scope='function', name='model')
    def test_init(self, ):
        
        id = np.arange(9)
        mol = np.array([0, 1, 1, 2, 2, 2, 3, 3, 3])
        position = np.random.random((9, 3))
        
        m = Model()
        m.appendFields(dict(id=id, mol=mol, position=position))
        yield m
        
    def test_get(self, model):
        
        fields = model.fields
        assert len(fields) == 3
        
        dtype = model.dtype
        assert dtype
        
        assert 'id' in model
        id = model.id
        npt.assert_equal(id, np.arange(9)) 
        
        models = model.groupby('mol')
        assert len(models) == 4