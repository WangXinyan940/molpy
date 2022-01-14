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
        at1 = ff.defAtomType('at1', 'atcA', dict(charge=0.123, mass=1.234))
        at2 = ff.defAtomType('at2', 'atcA', dict(charge=0.234, mass=2.345))
        at3 = ff.defAtomType('at3', 'atcA', dict(charge=0.234, mass=2.345))
        at4 = ff.defAtomType('at4', 'atcA', dict(charge=0.234, mass=2.345))
        
        bt1 = ff.defBondType('bt1', at1, at1, 'btcA', dict(length=1.53, k=0.8))
        bt1 = ff.defBondType('bt2', at1, at2, 'btcA', dict(length=1.53, k=0.8))
        bt1 = ff.defBondType('bt3', at2, at2, 'btcA', dict(length=1.53, k=0.8))
        
        yield ff
        
    def test_match_atomtype_of_atoms(self, ff, atoms):
        
        atoms = ff.matchAtomTypeOfAtoms(atoms, field='type', ref='name')
        assert 'atomType' in atoms.fields
    
    def test_match_bondtype_of_atoms(self, ff, atoms):
        if 'atomType' not in atoms:
            atoms = ff.matchAtomTypeOfAtoms(atoms, field='type', ref='name')
        atoms = ff.matchBondTypeOfAtoms(atoms)
        print(atoms)
        