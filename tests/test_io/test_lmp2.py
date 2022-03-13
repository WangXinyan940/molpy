# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-12
# version: 0.0.1

import pytest
from molpy.io.lmp2 import DumpReader, DataReader
import numpy.testing as npt
import numpy as np

class TestDump:
    
    @pytest.fixture(scope='class', name='dump')
    def test_init(self):
        
        dump = DumpReader('tests/data/linear.dump')
        yield dump
        
    def test_get_frame(self, dump):
        
        data = dump.getframe(2)
        assert data['timestep'] == 20
        assert data['natoms'] == 60
        atomInfo = data['atomInfo']
        npt.assert_allclose(np.asfarray(list(atomInfo[-1])), np.array('45 18 6 -11.8 2.37502 43.1304 46.726'.split(), dtype=float))
        
class TestData:
    
    @pytest.fixture(scope='class', name='data')
    def test_init(self):
        
        data = DataReader('tests/data/linear.data')
        yield data
        
    def test_parse_line(self):
        
        line = '\t60 Atom\n# comment'
        line = DataReader.parse_line(line)
        assert line == ['60', 'Atom']
        
        line = ''
        line = DataReader.parse_line(line)
        assert line != ['']
        
    def test_parse(self, data):
        
        data = data.getdata()
        atoms = data['Atoms']
        
        npt.assert_allclose(np.asfarray(list(atoms[-1])), np.array('60	33	6	-11.8000	40.2637	47.8022	 6.3059'.split(), dtype=float))
        
        bonds = data['Bonds']
        assert bonds[0] == [1, 1, 1, 2]
        
