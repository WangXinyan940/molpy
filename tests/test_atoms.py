# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.1

import pytest
import numpy as np
import numpy.testing as npt
from molpy.atoms import AtomManager, Atoms


class TestAtoms:
 
    def test_group_by(self, atoms):
        groups = atoms.groupby('mol')
        assert len(groups) == 3
        
    def test_get_atom_instances(self, atoms):
        atomInstances = atoms.getAtoms()
        assert len(atomInstances) == atoms.natoms
        assert atomInstances[0].id == 0
        
    def test_calc_center_of_mass(self):
        
        positions = np.zeros((6, 3))
        positions[:, 0] = np.arange(6)
        atoms = Atoms(dict(id=np.arange(6), position=positions))
        npt.assert_equal(atoms.calcCenterOfMass(), np.array([2.5, 0, 0]))
        
    def test_calc_raduis_of_gyration(self):
        
        # linear
        positions = np.zeros((60, 3))
        positions[:, 0] = np.arange(60)
        atoms = Atoms(dict(id=np.arange(60), position=positions))
        npt.assert_allclose(atoms.calcRadiusOfGyration(), 17.318102)
        
        # circle
        positions = np.zeros((60, 3))
        theta = 2*np.arange(60)*np.pi/60
        positions[:, 0] = np.cos(theta)
        positions[:, 1] = np.sin(theta)
        atoms = Atoms(dict(id=np.arange(60), position=positions))
        npt.assert_allclose(atoms.calcRadiusOfGyration(), 1)
        
    def test_add_atoms(self):

        positions = np.zeros((60, 3))
        positions[:, 0] = np.arange(60)
        atoms1 = Atoms(dict(id=np.arange(60), position=positions))    
        
        positions = np.zeros((6, 3))
        positions[:, 0] = np.arange(6)
        atoms2 = Atoms(dict(id=np.arange(6), position=positions))           
        
        atoms1.append(atoms2)
        assert atoms1.natoms == 66 
        

                    
        
class TestAtomManager:
    
    @pytest.fixture(scope='class', name='am')
    def test_init(self):
        atomManager = AtomManager()
        assert atomManager.atoms.natoms == 0
        assert atomManager.molecules.__len__() == 0
        return atomManager
        
    def test_register_type(self, am):
        
        am.registerType('NewType')
        assert len(am.newTypes) == 0
