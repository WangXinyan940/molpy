# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

import pytest
import numpy as np
from molpy.atoms import Atoms
from molpy.bond import Bond
from molpy.topo import Topo

class TestTopoWithoutAtom:
    
    @pytest.fixture(scope='class', name='topo')
    def test_init(self):
        
        rawTopo = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3]
        }
        
        topo = Topo(rawTopo)
        yield topo
        
    def test_get_bonds(self, topo):
        
        bonds = topo.getBonds()
        assert len(bonds) == bonds.nbonds == 4
        
        
class TestTopoWithAtom:
    
    @pytest.fixture(scope='class', name='atoms')
    def init_data(self):
        
        atoms = Atoms(5, [('id', int), ('position', float, (3, ))], group=[1,2,3,4,5], vel=np.random.random((5, 3)))
        
        yield atoms
    
    @pytest.fixture(scope='class', name='topo')
    def test_init(self, atoms):
        
        rawTopo = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3]
        }
        
        topo = Topo(rawTopo, atoms.data)
        yield topo
        
    def test_get_bonds(self, topo, atoms):
        
        bonds = topo.getBonds()
        bondInstances = bonds.getBondInstances()
