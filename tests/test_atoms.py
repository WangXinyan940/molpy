# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-05-25
# version: 0.0.1

from molpy import Atoms
import numpy as np
import numpy.testing as npt

class TestAtoms:
    
    def test_getPositions(self):
        rng = np.random.default_rng(41)
        atoms = Atoms('test')
        atoms['positions'] = rng.uniform(0, 1, size=(10, 3))
        positions = atoms.getPositions()
        npt.assert_array_equal(positions, atoms['positions'])
        
        atoms = Atoms('test')
        atoms['x'] = np.random.uniform(0, 1, size=(10,))
        atoms['y'] = np.random.uniform(0, 1, size=(10,))
        atoms['z'] = np.random.uniform(0, 1, size=(10,))
        positions = np.stack((atoms['x'], atoms['y'], atoms['z']), axis=0).T
        npt.assert_array_equal(positions, atoms.getPositions())
    
    def test_split(self):
        
        atoms = Atoms('test')
        positions = np.random.normal(0,1, size=(10, 3))
        atoms['positions'] = positions
        segment_ids = [[0, 1, 2], [3, 4, 5], [6, 7], [8, 9]]
        atoms_list = atoms.split(segment_ids)
        assert len(atoms_list) == 4
        assert atoms_list[0].nnodes == 3
        npt.assert_array_equal(atoms_list[0]['positions'], positions[:3])
        
        