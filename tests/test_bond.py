# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.1

import pytest
import numpy as np
from molpy.atom import Atom
from molpy.bond import Bond
from molpy.forcefield import BondType


class TestBond:
    
    @pytest.fixture(scope='class', name='bond')
    def test_init(self):
        itom = Atom({'position': np.array([0, 0, 0])})
        jtom = Atom({'position': np.array([1, 0, 0])})
        bond = Bond(itom, jtom)
        bondType = BondType('harmonic')
        bondType.properties.update({'k': 1, 'r0': 1})
        bond.setBondType(bondType)
        return bond
    
    def test_getEnergy(self, bond):
        assert bond.getEnergy(2) == 0.5