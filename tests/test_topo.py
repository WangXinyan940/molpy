# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-06
# version: 0.0.1

import src
import pytest
from src.molpy.topo import Topo
import numpy.testing as npt

class TestTopo:
    
    @pytest.fixture(scope="class", name='linear')
    def init_linear(self):
        
        yield Topo(6)
        
    @pytest.fixture(scope='class', name='cyclic')
    def init_cyclic(self):
        
        yield Topo(6)
        
    def test_set_topo(self, linear, cyclic):
        
        connect = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
        linear.set_topo(connect)
        connect = {
            0: [5, 1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4, 0]
        }
        cyclic.set_topo(connect)
        
        assert linear.nEdge == 5
        assert cyclic.nEdge == 6
        
    def test_get_sub_topo(self, linear, cyclic):
        pass
    
    def test_valid_adj_dict(self):
        connect = {
            0: [5, 1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4, 0]
        }
        adjList, adjDict, adjMat = Topo.valid_adj_dict(connect)

    
    def test_valid_adj_list(self):
        connect = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
        adjList, adjDict, adjMat = Topo.valid_adj_list(connect)
        
    def test_get_two_bodies(self, linear, cyclic):
        connection = linear.get_two_bodies()
        
        assert len(connection) == linear.nTwoBodies
        
        connection = cyclic.get_two_bodies()
        assert len(connection) == cyclic.nTwoBodies
        
    def test_get_three_bodies(self, linear, cyclic):
        connection = linear.get_three_bodies()
        
        assert len(connection) == linear.nThreeBodies
        
        connection = cyclic.get_three_bodies()
        assert len(connection) == cyclic.nThreeBodies
        
    def test_get_four_bodies(self, linear, cyclic):
        connection = linear.get_four_bodies()
        
        assert len(connection) == linear.nFourBodies
        
        connection = cyclic.get_four_bodies()
        assert len(connection) == cyclic.nFourBodies