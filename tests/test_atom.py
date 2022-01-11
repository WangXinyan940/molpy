# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.1

import pytest
import numpy as np
import numpy.testing as npt
from molpy.atom import Atom

class TestAtom:
    
    def test_init(self):
        atom = Atom()
        atom.appendFields(dict(q=0, atomid=0))
        assert atom.q == 0
        assert atom.atomid == 0
        assert atom.dtype
        

        
        