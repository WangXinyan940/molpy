import pytest
import numpy as np
import numpy.testing as npt
from arrayTest import Array2i, Array2f

class TestArray:
    
    @pytest.fixture(name='zeros')
    def zeros_fixture(self):
        return Array2i(5, 3)
    
    def test_shape(self, zeros):
        z = np.array(zeros)
        assert z.shape == (5, 3)