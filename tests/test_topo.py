# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-12
# version: 0.0.1

import numpy as np
import numpy.testing as npt
import pytest
from molpy.topo import Topo


class TestTopo:
    
    def test_add_edge(self):
        
        topo = Topo()
        topo.add_edge(0, 1)
        assert topo._edges[0] == {1}
        assert topo._edges[1] == {0}
        topo.add_edge(0, 2)
        assert topo._edges[0] == {1, 2}
        
        offset = 3
        topo.add_edge(0, 1, offset)
        assert topo._edges[3] == {4}
        assert topo._edges[4] == {3}
    
    def test_init_via_adjList(self):

        adjList = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 8],
            [8, 9],
        ]
        topo = Topo()
        topo.set_topo_by_adjList(adjList)
        assert topo.n_edges == 9

    def test_init_via_adjDict(self):

        adjDict = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4, 6],
            6: [5, 7],
            7: [6, 8],
            8: [7, 9],
            9: [8],
        }
        topo = Topo()
        topo.set_topo_by_adjDict(adjDict)
        assert topo.n_edges == 9

    @pytest.fixture(scope="class", name="linear")
    def init_linear_topo(self):

        adjList = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 8],
            [8, 9],
        ]
        topo = Topo()
        topo.set_topo_by_adjList(adjList)
        yield topo

    @pytest.fixture(scope="class", name="cyclic")
    def init_cyclic_topo(self):

        adjList = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 8],
            [8, 9],
            [9, 0],
        ]
        topo = Topo()
        topo.set_topo_by_adjList(adjList)
        yield topo
        
    def test_get_two_bodies(self, linear, cyclic):

        two = linear.get_two_bodies()
        assert len(two) == 9
        two = cyclic.get_two_bodies()
        assert len(two) == 10

    def test_get_three_bodies(self, linear, cyclic):

        three = linear.get_three_bodies()
        assert len(three) == 8
        three = cyclic.get_three_bodies()
        assert len(three) == 10

    def test_get_four_bodies(self, linear, cyclic):

        four = linear.get_four_bodies()
        assert len(four) == 7
        four = cyclic.get_four_bodies()
        assert len(four) == 10

    def test_append(self):
        
        adjList = [
            [0, 1],
            [1, 2],
            [2, 3],
        ]
        
        topo = Topo()
        topo.set_topo_by_adjList(adjList)
        
        adjList = [
            [0, 1],  # [4, 5]
            [1, 2],  # [5, 6]
            [2, 3],  # [6, 7]
        ]
        topo1 = Topo()
        topo1.set_topo_by_adjList(adjList)
        
        topo.append(topo1)
        topo.add_edge(3, 4)  # [3, 4]
        assert topo.n_edges == 7
        assert topo._edges[3] == {2, 4}
        assert topo._edges[7] == {6}