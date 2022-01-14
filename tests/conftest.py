# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.2

import pytest
import numpy as np
from molpy.atoms import Atoms

natoms = 5
@pytest.fixture(scope='module', name='atoms')
def test_init():
    atoms = Atoms(5, dict(id=np.arange(natoms), mol=np.array([0, 0, 1, 1, 2]), type=np.array(['at1', 'at1', 'at2', 'at1', 'at2']), position=np.random.random((natoms, 3))), connection=[[0, 1], [1, 2], [2, 3], [3, 4]])
    assert 'id' in atoms.fields
    assert 'mol' in atoms.fields
    assert atoms.natoms == 5
    yield atoms