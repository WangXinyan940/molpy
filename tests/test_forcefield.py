# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-12
# version: 0.0.1

import pytest
from molpy.forcefield import ForceField
import molpy as mp
import numpy as np

class TestForceField:
    
    @pytest.fixture(scope='class', name='ff')
    def test_init(self):
        
        ff = ForceField()
        at1 = ff.defAtomType('at1', charge=0.123, mass=1.234)
        at1.queryFunc = lambda x: x['type'] == 'at1'
        at2 = ff.defAtomType('at2', charge=0.234, mass=2.345)
        at2.queryFunc = lambda x: x['type'] == 'at2'

        # at3 = ff.defAtomType('at3', charge=0.234, mass=2.345)
        # at4 = ff.defAtomType('at4', charge=0.234, mass=2.345)
        
        bt1 = ff.defBondType('bt1', length=1.53, k=0.8)
        def f(x):
            b1 = x[0]['type'] == 'at1'
            b2 = x[1]['type'] == 'at1'
            return b1 and b2
        # bt1.queryFunc = lambda x: x[0]['type'] == 'at1' and x[1]['type'] == 'at1'
        bt1.queryFunc = f
        bt2 = ff.defBondType('bt2', length=1.53, k=0.8)
        bt2.queryFunc = lambda x: (x[0]['type'] == 'at1' and x[1]['type'] == 'at2') or (x[0]['type'] == 'at2' and x[1]['type'] == 'at1')
        bt3 = ff.defBondType('bt3', length=1.53, k=0.8)
        bt3.queryFunc = lambda x: x[0]['type'] == 'at2' and x[1]['type'] == 'at2'

        pr1 = ff.defPairType('pr1', sigma=0.4, epsilon=4)
        pr1.queryFunc = lambda x: True
        
        yield ff
        
    def test_query_atomtypes(self, ff, atoms):
        
        atomTypes = ff.queryAtomTypes(atoms)

    
    def test_query_bondTypes(self, ff, atoms):

        bondTypes = ff.queryBondTypes(atoms)
        
    def test_query_pairTypes(self, ff, atoms):

        box = mp.Box.cube(10)
        pairTypes = ff.queryPairTypes(atoms, box, 4)
        