# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.1

import pytest
import numpy as np

from molpy.bond import Bonds
from molpy.atoms import Atoms

class TestBonds:
    
    @pytest.fixture(scope='class', name='atoms')
    def init_data(self):
        
        atoms = Atoms(5, [('id', int), ('position', float, (3, ))], group=[1,2,3,4,5], vel=np.random.random((5, 3)))
        
        yield atoms
    
    @pytest.fixture(scope='class', name='bonds')
    def test_init(self, atoms):
        
        rawBonds = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 0]]
        bonds = Bonds(rawBonds, atoms.atomInstances)
        assert bonds.nbonds == len(bonds) == 4
        yield bonds
        
    def test_get_bond_instances(self, bonds, atoms):
        
        bondInstances = bonds.getBondInstances()
        assert len(bondInstances) == 4
        assert bondInstances[1].itom.id == 0
        atoms.id = np.arange(5)
        assert bondInstances[1].itom.id == 1
        atoms.id = np.array([9, 9, 9, 9, 9])
        assert bondInstances[1].itom.id == 9
        assert bondInstances[1].itom.data.dtype != np.dtype(object)