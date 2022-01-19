# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.1

import pytest
import numpy as np
import numpy.testing as npt
from molpy.atoms import Atoms


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
        
    def test_calc_center_of_mass(self):
        
        positions = np.zeros((6, 3))
        positions[:, 0] = np.arange(6)
        atoms = Atoms(6, dict(id=np.arange(6), position=positions))
        npt.assert_equal(atoms.calcCenterOfMass(), np.array([2.5, 0, 0]))
        
    def test_calc_raduis_of_gyration(self):
        
        # linear
        positions = np.zeros((60, 3))
        positions[:, 0] = np.arange(60)
        atoms = Atoms(60, dict(id=np.arange(60), position=positions))
        npt.assert_allclose(atoms.calcRadiusOfGyration(), 17.318102)
        
        # circle
        positions = np.zeros((60, 3))
        theta = 2*np.arange(60)*np.pi/60
        positions[:, 0] = np.cos(theta)
        positions[:, 1] = np.sin(theta)
        atoms = Atoms(60, dict(id=np.arange(60), position=positions))
        npt.assert_allclose(atoms.calcRadiusOfGyration(), 1)

                    
        
class TestAtomsSelections:
        
    def test_select_by_func(self, atoms):
        
        def func(data):
            return data['mol'] == 1
        
        newAtoms = atoms.selectByFunc(func)
        npt.assert_equal(newAtoms.id, [2, 3])
        opos = newAtoms.position
        atoms.position = np.random.random((5, 3))
        npt.assert_equal(newAtoms.position, opos)
        
        