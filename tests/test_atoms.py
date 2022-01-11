# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.1

import pytest
import numpy as np
import numpy.testing as npt
from molpy.atoms import Atoms

        
class TestAtoms:
    
    @pytest.fixture(name='atoms')
    def test_init(self):
        atoms = Atoms(5, [('id', int), ('position', float, (3, ))], group=[1, 0, 2, 1, 0], vel=np.random.random((5, 3)))
        assert len(atoms.getAtomInstances()) == 5
        yield atoms
        
    def test_sync(self, atoms):
        
        npt.assert_equal(atoms.id, np.zeros(5))
        atomList = atoms.getAtomInstances()

        assert atomList[-1].data['id'] == 0
        atoms.data['id'] = np.arange(5)
        assert atoms.data[-1]['id'] == 4
        assert atomList[-1].data['id'] == 4
        
    def test_group_by(self, atoms):
        groups = atoms.groupby('group')
        assert len(groups) == 3
        
class TestAtomsSelections:
    
    @pytest.fixture(name='atoms', scope='function')
    def atoms(self):
        atoms = Atoms(5, [('id', int), ('molid', int), ('position', float, (3, ))])
        atoms.id = np.arange(5)
        atoms.molid = np.array([1,2,2,3,3])
        atoms.position = np.random.random((5, 3))
        yield atoms
        
    def test_select_by_func(self, atoms):
        
        def func(data):
            return data['molid'] == 3
        
        newAtoms = atoms.selectByFunc(func)
        npt.assert_equal(newAtoms.id, [3,4])
        opos = newAtoms.position
        atoms.position = np.random.random((5, 3))
        npt.assert_equal(newAtoms.position, opos)
        
        