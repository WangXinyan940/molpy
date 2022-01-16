# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.1

import pytest
import numpy as np
import numpy.testing as npt


class TestAtoms:
 
    def test_group_by(self, atoms):
        groups = atoms.groupby('mol')
        assert len(groups) == 3
        
    def test_get_atom_instances(self, atoms):
        atomInstances = atoms.getAtoms()
        assert len(atomInstances) == atoms.natoms
        assert atomInstances[0].id == 0
        
    def test_init_topo(self, atoms):
        bonds = atoms.getBondIdx()
        assert len(bonds) == 4
        angles = atoms.getAngleIdx()
        assert len(angles) == 3
        dihedrals = atoms.getDihedralIdx()
        assert len(dihedrals) == 2
        
class TestAtomsSelections:
        
    def test_select_by_func(self, atoms):
        
        def func(data):
            return data['mol'] == 1
        
        newAtoms = atoms.selectByFunc(func)
        npt.assert_equal(newAtoms.id, [2, 3])
        opos = newAtoms.position
        atoms.position = np.random.random((5, 3))
        npt.assert_equal(newAtoms.position, opos)
        
        