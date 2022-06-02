# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from .topo import Topo
from copy import deepcopy

class Graph:
    
    def __init__(self, name) -> None:
        
        self.name = name if name is not None else str(id(self))[-5:]
        self.topo:Topo = Topo()
        self.nodes:dict = {}
        self.edges:dict = {}
        self.globals:dict = {}
        
    @classmethod
    def fromCopy(cls, graph):
        ins = cls(graph.name)
        ins.nodes = deepcopy(graph.nodes)
        ins.globals = deepcopy(graph.globals)
        ins.edges = deepcopy(graph.edges)
        ins.topo = deepcopy(graph.topo)
        return ins
        
    @property
    def nnodes(self)->int:
        try:
            value = len(next(iter(self.nodes.values())))
        except:
            value = 0
        return value
        
    def __getitem__(self, key):
        
        if isinstance(key, str):
            if key == 'adjList':
                return self.topo.adjList
            elif key == 'adjDict':
                return self.topo.adjDict
            return self.nodes[key]
        else:
            return self.getSubGraph(key)
        
    def getSubGraph(self, index):
            
        ins = Graph(self.name)
        ins.topo = self.topo.getSubTopo(self.nnodes, index)
        ins.nodes = {k: v[index] for k, v in self.nodes.items()}
        # ins.edges = {k: v[index] for k, v in self.edges.items()}
        # ins.globals = {k: v[index] for k, v in self.globals.items()}
        return ins
    
    def __setitem__(self, key, value):
        
        self.nodes[key] = value
        self.isAlign()
        
    def __contains__(self, item):
        
        return item in self.nodes
        
    def __len__(self):
        return self.nnodes
    
    def isAlign(self)->bool:
        pass
    
    def __repr__(self):
        
        return f'<{self.__class__.__name__} {self.name} with len {len(self)}>'
    
    __str__ = __repr__
    
    def replaceNodes(self, **fields):
        
        for k, v in fields.items():
            self.nodes[k] = v
            
    def replaceEdges(self, **fields):
        
        for k, v in fields.items():
            self.edges[k] = v
            
    def replaceGlobals(self, **fields):
        
        for k, v in fields.items():
            self.globals[k] = v
            
    def replace(self, graph):
        """using provided graph's features to replace self's features


        Args:
            graph (Graph): 
        """
        self.replaceNodes(**graph.nodes)
        self.replaceEdges(**graph.edges)
        self.replaceGlobals(**graph.globals)
        self.topo = graph.topo
        
    def setTopo(self, connection):
        self.topo.setTopo(connection)