# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-12
# version: 0.0.1

from molpy.graph import Graph
import numpy.typing as npt

class Atoms(Graph):
    
    def __init__(self, withTopo=False):
        
        super().__init__(withTopo)
    
    def set_atom_values(self, key:str, value:npt.ArrayLike, ref:npt.ArrayLike):
        
        self.set_node_value(key, value, ref)
        
    @property
    def n_atoms(self):
        return self._n_nodes

    
class AtomVec(Atoms):
    
    def __init__(self, ):
        
        super().__init__()
        
        self.molecules = []
        
    
        