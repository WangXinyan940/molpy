# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-05-31
# version: 0.0.1

import pytest
from molpy.topo import Topo

class TestTopo:
    
    @pytest.fixture(scope='class', name='linear')
    def init_linear(self):
        topo = Topo([[0,1], [1,2], [2,3], [3,4], [4,5]])
        return topo
    
    @pytest.fixture(scope='class', name='cyclic')
    def init_cyclic(self):
        topo = Topo([[0,1], [1,2], [2,3], [3,4], [4,5], [5,0]])
        return topo
    
    def test_getsub_linear(self, linear):
        sub = linear.getSubTopo(6, [0,1,2])
        assert sub.adjList == [[0,1], [1,2]]
        assert sub.adjDict == {0: [1], 1: [2]}
        
        sub = linear.getSubTopo(6, slice(0, 4))
        assert sub.adjList == [[0,1], [1,2], [2,3]]
        assert sub.adjDict == {0: [1], 1: [2], 2: [3]}
        
        sub = linear.getSubTopo(6, [True, True, True, True, False, False])
        assert sub.adjList == [[0,1], [1,2], [2,3]]
        assert sub.adjDict == {0: [1], 1: [2], 2: [3]}
                
        
    def test_getsub_cyclic(self, cyclic):
        sub = cyclic.getSubTopo(6, [0,1,2])
        assert sub.adjList == [[0,1], [1,2]]
        assert sub.adjDict == {0: [1], 1: [2]}
        
        sub = cyclic.getSubTopo(6, slice(0, 4))
        assert sub.adjList == [[0,1], [1,2], [2,3]]
        assert sub.adjDict == {0: [1], 1: [2], 2: [3]}
        
        sub = cyclic.getSubTopo(6, [True, True, True, True, False, False])
        assert sub.adjList == [[0,1], [1,2], [2,3]]
        assert sub.adjDict == {0: [1], 1: [2], 2: [3]}        