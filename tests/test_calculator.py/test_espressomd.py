# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-02
# version: 0.0.1

import pytest
from molpy.modeller.randomWalk import RandomWalkOnFcc

class TestEspressomd:
    
    @pytest.fixture(scope='class')
    def __init__(self) -> None:
        rw = RandomWalkOnFcc(10, 10, 10)
        self.positions = rw.walkOnce(rw.findStart(), 10, )
        