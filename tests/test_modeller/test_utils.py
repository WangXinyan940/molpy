# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-03
# version: 0.0.1

import pytest
from molpy.modeller.randomWalk import RandomWalkOnFcc
from molpy.modeller.utils import toAtoms


class TestUtils:
    
    @pytest.fixture(scope='class', name='rw')
    def initRandomWalk(self):
        return RandomWalkOnFcc(10, 10, 10)
    
    def test_toAtoms(self, rw):
        
        positions, bonds = rw.linear(10)
        
        atoms = toAtoms(positions, bonds)
        print(atoms.natoms)
        
        assert atoms.natoms == 10
        assert atoms.nbonds == 9
    
