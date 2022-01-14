# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-12
# version: 0.0.1

import pytest
from molpy.forcefield import ForceField

class TestForceField:
    
    @pytest.fixture(scope='class', name='ff')
    def test_init(self):
        
        ff = ForceField()
        ff.defAtomType('at1', 'atcA', dict(charge=0.123, mass=1.234))
        ff.defAtomType('at2', 'atcA', dict(charge=0.234, mass=2.345))
        
        yield ff
        
    def test_match_atomtype_of_atoms(self, ff, atoms):
        
        atoms = ff.matchAtomTypeOfAtoms(atoms, field='type', ref='name')
        assert 'atomType' in atoms.fields
    
    def test_match_bondtype_of_atoms(self, ff, atoms):
        atoms = ff.matchBondTypeOfAtoms(atoms)
        print(atoms)