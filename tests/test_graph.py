# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-11
# version: 0.0.1

import pytest
import numpy as np
import numpy.testing as npt
from molpy.graph import Graph

class TestNonTopoGraph:
    
    @pytest.fixture(scope='class', name='g')
    def init_non_topo_graph(self):
        
        graph = Graph(withTopo=False)
        graph.set_node('A', np.arange(10))
        graph.set_node('B', np.arange(10)+1)
        
        yield graph
        
    def test_get_node(self, g):
        
        npt.assert_equal(g.get_node('A'), np.arange(10))
        npt.assert_equal(g['B'], np.arange(10)+1)
        
    def test_slice(self, g):
        
        subg1 = g[:5]
        subg2 = g[::3]
        subg3 = g[2]
        
        npt.assert_equal(subg1.get_node('A'), np.arange(5))
        npt.assert_equal(subg2.get_node('A'), np.arange(10)[::3])
        npt.assert_equal(subg3.get_node('A'), np.arange(10)[2])
        
    def test_mask(self, g):
        
        mask = np.array([True, False, True, False, True, False, True, False, True, False])
        subg = g[mask]
        
        npt.assert_equal(subg.get_node('A'), np.arange(10)[mask])
        
    def test_get_subgraph(self, g):
        
        og = Graph(withTopo=False)
        og.set_node('A', np.arange(10)+10)
        og.set_node('B', np.arange(10)+11)
        
        og.append(g)
        assert og.n_nodes == 20

    def test_set_value(self):

        graph = Graph()
        ids = np.array([1,4,2,3,5])
        value = np.array([1,4,2,3,5])
        graph.set_node('value', value, ids)

        npt.assert_equal(graph['value'], np.arange(5)+1)
        
        