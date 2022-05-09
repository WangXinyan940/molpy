# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from .topo import Topo

class Graph:
    
    def __init__(self, name) -> None:
        
        self.name = name if name is not None else id(self)
        self.topo = Topo()
        self.nodes = {}
        self.globals = {}
        self.edges = {}
        
    @property
    def nnodes(self):
        
        value = next(iter(self.nodes.values()))
        return len(value)
        
    def __getitem__(self, key):
        
        return self.nodes[key]
    
    def __setitem__(self, key, value):
        
        self.nodes[key] = value
        self.isAlign()
        
    def __len__(self):
        return self.nnodes
    
    def isAlign(self)->bool:
        pass
    
    def __repr__(self):
        
        return f'<{self.__class__.__name__} {self.name} with len {len(self)}>'
    
    __str__ = __repr__
    
    
    
    