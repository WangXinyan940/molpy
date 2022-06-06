# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-06
# version: 0.0.1

import numpy as np
from typing import List, Dict, Tuple, Union, NoReturn
from collections import defaultdict
from itertools import combinations


class Topo:
    
    """ A class for topology in the graph. \
        In the chemstry, this class represents \
            bonds/angles/dihedrals etc. in a molecule. \
            After providing the connection, it can reason topo info of a molecule.
    """
    
    def __init__(self, nVex:int):
        """ Initialize a topology class with connection in graph, \
                and reason topo info. \
            The connection can be adjDict, adjList, adjMatrix, or None. \
            The adjList is a list of lists, adjDict is a dict of list, \
                and adjMatrix is a numpy array.
        
        For example, we have a star type of graph, \
            we can use the following connection format to create a topology:
        
        adjList:
            [[0, 1], [0, 2], [0, 3], [0, 4]]
        adjDict:
            {0: [1, 2, 3, 4]}
        adjMatrix:
            [[0, 1, 1, 1, 1],
             [1, 0, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 0, 0, 0, 0]]
             
        In the adjList and adjDict, the index of the atoms is the same as the index of the atoms in the graph/molecule, i.e. the first atom in the molecule is the 0th atom in the adjList and adjDict.
        
        If no special notation, the following docs and examples are used star type of graph as an example
        Args:
            connection (adjList/adjDict, optional): connection between nodes. Defaults to None, which means an empty topo class.
            special_bonds (Sequence, optional): _description_. Defaults to None.
        """        
        self._nVex:int = nVex
        self._adjDict:dict = {}
        
    @property
    def nVex(self)->int:
        """ Number of vertices in the graph.

        Returns:
            int: Number of vertices
        """
        return self._nVex
        
    def set_topo(self, connection: Union[List[List[int]], Dict[int, List[int]]])->NoReturn:
        
        if isinstance(connection, List):
            adjDict, adjList, adjMatrix = Topo.valid_adj_dict(connection)  #
        elif isinstance(connection, Dict):
            adjDict, adjList, adjMatrix = Topo.valid_adj_list(connection)
        else:
            raise TypeError(f'{type(connection)} is unacceptable topo format')
        
        self._adjDict = adjDict
        self._adjList = adjList
        
    @staticmethod
    def valid_adj_dict(connection: Dict[int, List[int]])->Tuple:
        return connection, [[c, p] for c, ps in connection.items() for p in ps], None
    
    @staticmethod
    def valid_adj_list(connection: List[List[int]])->Tuple:
        connection = defaultdict(list)
        for bond in connection:
            connection[bond[0]].append(bond[1])
            connection[bond[1]].append(bond[0])
        return dict(connection), connection, None
    
    def get_two_bodies(self)->np.ndarray:
        """ get connected two vertices in the topo
            e.g. return np.array([[0, 1], [0, 2], [0, 3], [0, 4]])

        Returns:
            np.ndarray: two bodies index
        """
        topo = self._adjDict
        rawBonds = []
        for c, ps in topo.items():
            for p in ps:
                rawBonds.append([c, p])

        # remove duplicates
        rawBonds = np.asarray(rawBonds)
        rawBonds = np.sort(rawBonds, axis=1)
        bonds = np.unique(rawBonds, axis=0) 
        return bonds      
    
    def get_three_bodies(self)->np.ndarray:
        """ get connected three vertrices in the topo
            e.g. return np.array([[0,1,2], [1,2,3], [2,3,4]])

        Returns:
            np.ndarray: three bodies index
        """

        topo = self._adjDict
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
    
    def get_four_bodies(self)->np.ndarray:
        """ get connected three vertrices in the topo
            e.g. return np.array([[0,1,2,3], [1,2,3,4]])

        Returns:
            np.ndarray: four bodies index
        """
     
        topo = self._adjDict
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
    def nTwoBodies(self):
        return len(self.get_two_bodies())
    
    @property
    def nThreeBodies(self):
        return len(self.get_three_bodies())
    
    @property
    def nFourBodies(self):
        return len(self.get_four_bodies())
    
    @property
    def twoBodies(self):
        return self.get_two_bodies()
    
    @property
    def threeBodies(self):
        return self.get_three_bodies()
    
    @property
    def fourBodies(self):
        return self.get_four_bodies()
    