# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-11-17
# version: 0.0.1

import pytest
import molpy as mp
import numpy as np
from molpy.ioapi import toLAMMPS
    
class TestLAMMPS:
    
    def test_write_ch4(self, H2O, SPCEforcefield):
        
        system = mp.System('h2o')
        system.cell = mp.Cell(3, 'ppp', xlo=0, xhi=35, ylo=0, yhi=35, zlo=0, zhi=35)
        system.forcefield = SPCEforcefield
        l = 1
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    h2o = H2O(name=f'h2o{l}').move(np.array([3.10*i, 3.10*j, 3.10*k]))
                    system.addMolecule(h2o)
                    l += 1
        system.mapping()
        system.complete()        
        toLAMMPS('lmp.data.test', system, atom_style='full')
        