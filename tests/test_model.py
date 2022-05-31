# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-05-31
# version: 0.0.1

import pytest
import numpy as np
from molpy.model import Graph
import numpy.testing as npt

class TestGraph:
    
    def test_getsubgraph(self):
    
        rng = np.random.default_rng(41)
        graph = Graph('test')
        graph.setTopo([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 0]])
        
        positions = rng.uniform(0, 1, size=(10, 3))
        graph['positions'] = positions
        
        npt.assert_equal(graph[:5]['positions'], positions[:5])
        npt.assert_equal(graph[::2]['positions'], positions[::2])
        mask = rng.uniform(0, 1, size=(10,)) > 0.5
        npt.assert_equal(graph[mask]['positions'], positions[mask])
        
        npt.assert_equal(graph[5:]['adjList'], [[0, 1], [1, 2], [2, 3], [3, 4]])