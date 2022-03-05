# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-03
# version: 0.0.1

import numpy as np
import pytest
from molpy.modeller.randomWalk import RandomWalk, RandomWalkOnFcc

class TestRandomWalk:
    
    @pytest.fixture(scope='class', name='rw')
    def initRandomWalk(self):
        return RandomWalkOnFcc(10, 10, 10)
    
    def test_init(self, rw):
        assert rw.rng is not None
        
    def test_walkOnce(self, rw):
        start = rw.findStart()
        positions, bonds = rw.walkOnce(start, nsteps=5)
        assert len(positions) == 5
        assert len(bonds) == 4
        
    def test_walkOnce_exclude(self, rw):
        start = rw.findStart()
        positions, bonds = rw.walkOnce(start, nsteps=5, exclude_start=True)
        assert len(positions) == 5
        assert len(bonds) == 4
        positions, bonds = rw.walkOnce(start, nsteps=5, exclude_start=False)
        assert np.array_equal(positions[0], rw.site2coord(start))
        
    def test_linear(self, rw):
        positions, bonds = rw.linear(10)
        assert len(positions) == 10
        assert len(bonds) == 9
        
    def test_graft(self, rw):
        positions, bonds = rw.graft(40, [3]*4, [5, 15, 25, 35])
        assert len(positions) == 52
        assert len(bonds) == 51
        