# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-12
# version: 0.0.1

import pytest
from molpy.io.lmp2 import DumpReader
import numpy.testing as npt
import numpy as np

class TestDump:
    
    @pytest.fixture(scope='class', name='dump')
    def test_init(self):
        
        dump = DumpReader('tests/data/linear.dump')
        yield dump
        
    def test_get_frame(self, dump):
        
        data = dump.getFrame(2)
        assert data['timestep'] == 20
        assert data['natoms'] == 60
        atomInfo = data['atomInfo']
        npt.assert_allclose(np.asfarray(list(atomInfo[-1])), np.array('45 18 6 -11.8 2.37502 43.1304 46.726'.split(), dtype=float))
        
        