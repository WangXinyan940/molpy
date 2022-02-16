# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

import pytest
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
        
        topo = Topo(connection=rawTopo)
        yield topo
        
    def test_get_bonds(self, topo):
        
        bonds = topo.getBonds()
        assert len(bonds) == bonds.nbonds == 4
        
        
class TestTopoWithAtom:
    
    @pytest.fixture(scope='class', name='topo')
    def test_init_topo(self, atoms):
        assert atoms.natoms == 5
        connection = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3]
        }
        
        topo = Topo(atoms, connection=connection)
        assert len(topo.adjList) == 8
        topo.setAtoms(atoms)
        yield topo
        
    def test_get_bonds(self, topo):
        
        bonds = topo.getBonds()
        assert bonds.nbonds == 4
