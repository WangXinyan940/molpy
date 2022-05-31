# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from collections import defaultdict
from itertools import combinations
from typing import Sequence
import numpy as np

class Topo:
    
    """ A class for topology in the graph. In the chemstry, this class represents bonds/angles/dihedrals etc. in a molecule. After providing the connection, it can reason topo info of a molecule.
    """
    
    def __init__(self, connection=None, special_bonds:Sequence=None):
        """ Initialize a topology class with connection in graph, and reason topo info. The connection can be adjDict, adjList, adjMatrix, or None. The adjList is a list of lists, adjDict is a dict of list, and adjMatrix is a numpy array.
        
        For example, we have a star type of graph, we can use the following connection format to create a topology:
        
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
        self.reset()
        self.setTopo(connection)
        self.special_bonds = special_bonds

    @property
    def adjDict(self):
        return self._adjDict

    @property
    def adjList(self):
        return self._adjList

    @property
    def adjMatrix(self):
        pass

    def reset(self):
        """reset the topo instance
        """
        self._atoms = None
        self._bonds = None
        self._angles = None
        self._dihedrals = None
        self._hasBond = False
        self._hasAngle = False
        self._hasDihedral = False    
        self._hasAtom = False
        
        self._bondTypes = None
        self._angleTypes = None
        self._dihedralsTypes = None
        
    def setTopo(self, connection):
        """convert connection to adjDict and adjList

        Args:
            connection (adjList/adjDict): input topo info

        Raises:
            TypeError: when input except connection format
        """
        # fall back to adjDict and adjList
        #! adjMatrix is not supported yet
        if connection is not None:
            if isinstance(connection, dict):
                adjDict, adjList, adjMatrix = self.__class__.validAdjDict(connection)
            elif isinstance(connection, (list, tuple)):
                adjDict, adjList, adjMatrix = self.__class__.validAdjList(connection)
            elif isinstance(connection, np.ndarray):
                adjDict, adjList, adjMatrix = self.__class__.validAdjList(connection)
            else:
                raise TypeError
            self._adjDict = adjDict
            self._adjList = adjList
            self._adjMatrix = adjMatrix
            
    def getSubTopo(self, index):
        """
        Get sub topology among index. For example, there is a topology like {1:{0,2}}, and we want to get the sub topology of [0, 1], then we can use getSubTopo([0, 1])
        
        Args:
            index (slice|list|np.array): vertices in the sub topology

        Returns:
            Topo: sub topo
        """
        adjDict = self._adjDict
        subtopo = defaultdict(list)
        
        nodei = np.sort(np.array(list(adjDict.keys())))[index]
        for i in nodei:
            for j in adjDict[i]:
                if j in nodei and j > i:
                    subtopo[i].append(j)
        
        return Topo(subtopo)

    @staticmethod
    def validAdjDict(conect):
        """ convert adjDict to adjList and adjMatrix

        Args:
            conect (adjDict): input adjDict

        Returns:
            (adjDict, adjList, adjMatrix)
        """
        return conect, [[c, p] for c, ps in conect.items() for p in ps], None
    
    @staticmethod
    def validAdjList(conect):
        """ convert adjList to adjDict and adjMatrix

        Args:
            conect (adjList): input adjList

        Returns:
            (adjDict, adjList, adjMatrix)            
        """
        connection = defaultdict(list)
        for bond in conect:
            connection[bond[0]].append(bond[1])
            connection[bond[1]].append(bond[0])
        return dict(connection), conect, None
        
    def getBonds(self)->np.ndarray:
        """get bonds representation from topo. 
           return np.array([[0, 1], [0, 2], [0, 3], [0, 4]])

        Returns:
            np.ndarray: bond info
        """
        if self._hasBond:
            return self._bonds
        
        topo = self._adjDict
        rawBonds = []
        for c, ps in topo.items():
            for p in ps:
                rawBonds.append([c, p])

        # remove duplicates
        rawBonds = np.array(rawBonds)
        rawBonds = np.sort(rawBonds, axis=1)
        bonds = np.unique(rawBonds, axis=0) 
        self._bonds = bonds
        self._hasBond = True
        return self._bonds
    
    def setBondTypes(self, bondtypes):
        """set bond types with identicial integers. The length of bondtypes should be equal to the number of bonds.

        Args:
            bondtypes (1-d List/np.ndarray): bond types

        Raises:
            ValueError: unknown format
        """
        
        if self._bondTypes is None or len(bondtypes) == len(self._bonds):
        
            self._bondTypes = np.array(bondtypes)
        else:
            raise ValueError
    
    @property
    def nbonds(self):
        self.getBonds()
        return len(self._bonds)
    
    def getAngles(self)->np.ndarray:
        
        if self._hasAngle:
            return self._angles

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
        self._angles = angles
        return angles
    
    @property
    def nangles(self):
        self.getAngles()
        return len(self._angles)
    
    def getDihedrals(self):
        
        if self._hasDihedral:
            return self._dihedrals
     
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
        self._dihedrals = dihedrals
        return dihedrals
    
    @property
    def ndihedrals(self)->np.ndarray:
        self.getDihedrals()
        return len(self._dihedrals)
    
    bonds = property(getBonds)
    angles = property(getAngles)
    dihedrals = property(getDihedrals)

 