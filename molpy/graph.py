# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-10
# version: 0.0.1

from typing import Dict, Optional, Union
import numpy as np
import numpy.typing as npt
from molpy.topo import Topo


class Graph:
    
    def __init__(self, withTopo:bool=False):
        
        self._n_nodes = 0
        self._topo: Optional[Topo] = Topo() if withTopo else None
        self._nodes: Dict[str, npt.NDArray] = {}  # 
        
    def set_node_value(self, key:str, value:npt.ArrayLike):
        
        v = np.array(value)
        self._n_nodes = max(self._n_nodes, len(v))
        self._nodes[key] = v
        
    def get_node_value(self, key:str)->npt.NDArray:
        
        return self._nodes[key]
        
    def get_subgraph(self, index: Union[slice, int, list, npt.NDArray]) -> 'Graph':
        
        graph = Graph.from_graph(self)
        nodes = {key: value[index] for key, value in self._nodes.items()}
        graph._nodes = nodes
        return graph
        
    def __getitem__(self, o: Union[str, slice, int, npt.NDArray]) -> Union['Graph', npt.NDArray]:
        
        if isinstance(o, str):
            return self.get_node_value(o)
        
        return self.get_subgraph(o)
    
    @classmethod
    def from_graph(cls, graph: 'Graph') -> 'Graph':
        
        ins = cls(graph._n_nodes)
        ins._nodes = graph._nodes
        return ins
    
    @property
    def n_nodes(self):
        return self._n_nodes
    
    @property
    def n_edges(self):
        if self._topo is None:
            return 0
        return self._topo.n_edges
    
    def __repr__(self)->str:
        
        if self._topo is None:
            return f'<Graph: {self._n_nodes} nodes>'
        else:
            return f'<Graph: {self._n_nodes} nodes, {self._topo.n_edges} edges>'
        
    