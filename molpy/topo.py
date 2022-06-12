# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-12
# version: 0.0.1

from typing import Dict, List
import numpy as np
import numpy.typing as npt
from itertools import combinations

class Topo:
    
    def __init__(self):
        
        self._edges:Dict[int, set(int)] = {}
        
    def set_topo_by_adjList(self, adjList:List[List[int]]):
        
        for edge in adjList:
            self.add_edge(edge[0], edge[1])
            
    def add_edge(self, i:int, j:int):
        
        if i not in self._edges:
            self._edges[i] = set()
        if j not in self._edges:
            self._edges[j] = set()
        self._edges[i].add(j)
        self._edges[j].add(i)
        
    def set_topo_by_adjDict(self, adjDict:Dict[int, List[int]]):
        
        for i, js in adjDict.items():
            for j in js:
                self.add_edge(i, j)
                
    def get_two_bodies(self)->npt.NDArray[np.int_]:
        
        topo = self._edges
        rawBonds = []
        for c, ps in topo.items():
            for p in ps:
                rawBonds.append([c, p])

        # remove duplicates
        bonds = np.unique(np.sort(np.array(rawBonds), axis=1), axis=0) 

        return bonds
    
    @property
    def n_edges(self)->int:
        return len(self.get_two_bodies())
    
    @property
    def n_two_bodies(self)->int:
        return len(self.get_two_bodies())       
    
    def get_three_bodies(self)->npt.NDArray[np.int_]:
        topo = self._edges
        rawAngles = []
        for c, ps in topo.items():
            if len(ps) < 2:
                continue
            for (itom, ktom) in combinations(ps, 2):
                rawAngles.append([itom, c, ktom])
        
        # remove duplicates
        angles = np.array(rawAngles)
        angles = np.where((angles[:,0]>angles[:,2]).reshape((-1, 1)), angles[:, ::-1], angles)
        angles = np.unique(angles, axis=0)

        return angles  
    
    @property
    def n_three_bodies(self)->int:
        return len(self.get_three_bodies())
        
    def get_four_bodies(self)->npt.NDArray[np.int_]:
        topo = self._edges
        rawDihes = []
        for jtom, ps in topo.items():
            if len(ps) < 2:
                continue
            for (itom, ktom) in combinations(ps, 2):
                
                for ltom in topo[itom]:
                    if ltom != jtom:
                        rawDihes.append([ltom, itom, jtom, ktom])
                for ltom in topo[ktom]:
                    if ltom != jtom:
                        rawDihes.append([itom, jtom, ktom, ltom])
        
        # remove duplicates
        dihedrals = np.array(rawDihes)
        dihedrals = np.where((dihedrals[:,1]>dihedrals[:,2]).reshape((-1, 1)), dihedrals[:, ::-1], dihedrals)
        dihedrals = np.unique(dihedrals, axis=0)

        return dihedrals  
    
    @property
    def n_four_bodies(self)->int:
        return len(self.get_four_bodies())