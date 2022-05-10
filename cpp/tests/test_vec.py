import pytest
from vec import Vec3i, Vec3f
import numpy as np
import numpy.testing as npt
    
class TestVec3:
    
    @pytest.fixture(name='zero')
    def test_vec3_default(self):
        return Vec3i()
    
    @pytest.fixture(name='one_i')
    def test_vec3_one_i(self):
        return Vec3i(1,1,1)
        
    @pytest.fixture(name='one_f')
    def test_vec3f_one(self):
        return Vec3f(1., 1., 1.)
    
    def test_vec3_repr(self, one_i):
        assert repr(one_i) == '<Vec3(1, 1, 1)>'
        
    def test_vec3_setter_getter(self, one_i):
        one_i.x = 2
        assert one_i.x == 2
    
    def test_vec3f(self, one_f):
        one_f.x = 1.1
        npt.assert_allclose(one_f.x, 1.1)
        
    def test_vec3_numpy(self, one_i):
        npt.assert_equal(np.array(one_i), np.array([1,1,1]))
        
    def test_vec3f_numpy(self, one_f):
        npt.assert_allclose(np.array(one_f), np.array([1.,1.,1.]))
