
from molpy.modeller.randomWalk import RandomWalkOnFcc
from molpy.modeller.utils import toAtoms
from molpy.system import System
import numpy as np
import pytest

class TestLMP:
    
    @pytest.fixture(scope='class', name='system')
    def test_init(self):
        
        system = System()
        
        rw = RandomWalkOnFcc(10, 10, 10)
        positions, bonds = rw.linear(10)
        atoms = toAtoms(positions, bonds)
        system._atoms = atoms
        
        return system
