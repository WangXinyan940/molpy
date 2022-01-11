# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-11
# version: 0.0.2

# TODO: new model to replace structure array

import pytest
import numpy as np
import numpy.testing as npt
from molpy.model import Model

natom = 9

class TestModel:

    
    @pytest.fixture(scope='function', name='model')
    def test_init(self, ):
        
        id = np.arange(natom)
        mol = np.array([0, 1, 1, 2, 2, 2, 3, 3, 3])
        position = np.random.random((natom, 3))
        
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
        npt.assert_equal(id, np.arange(natom)) 
        
        models = model.groupby('mol')
        assert len(models) == 4
        
    def test_set(self, model):
        
        newPos = np.random.random((natom, 3))
        model.position = newPos
        npt.assert_equal(model._fields['position'], newPos)
        
    def test_group_by(self, model):
        
        models = model.groupby('mol')
        assert len(models) == 4
        
    def test_to_structuredArray(self, model):
        data = model.toStructuredArray()
        assert len(data) == 9
        
    def test_check_alignment(self, model):
        model.appendFields({'test': np.arange(4)})
        assert not model.check_alignment()
        