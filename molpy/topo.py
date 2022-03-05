# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from collections import defaultdict
from itertools import combinations
import numpy as np

class Topo:
    
    def __init__(self, connection=None):
        
        self.reset()
        self.setTopo(connection)

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
        self._atoms = None
        self._bonds = None
        self._angles = None
        self._dihedrals = None
        self._hasBond = False
        self._hasAngle = False
        self._hasDihedral = False    
        self._hasAtom = False
        
    def setTopo(self, connection):
        if connection is not None:
            if isinstance(connection, dict):
                adjDict, adjList, adjMatrix = self.__class__.validAdjDict(connection)
            elif isinstance(connection, (list, tuple)):
                adjDict, adjList, adjMatrix = self.__class__.validAdjList(connection)
            else:
                raise TypeError
            self._adjDict = adjDict
            self._adjList = adjList
            self._adjMatrix = adjMatrix

    @staticmethod
    def validAdjDict(conect):
        
        return conect, [[c, p] for c, ps in conect.items() for p in ps], None
    
    @staticmethod
    def validAdjList(conect):

        connection = defaultdict(list)
        for bond in conect:
            connection[bond[0]].append(bond[1])
            connection[bond[1]].append(bond[0])
        return dict(connection), conect, None
        
    def getBonds(self):
        
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
        return self._bonds
    
    @property
    def nbonds(self):
        if not self._hasBond:
            self.getBonds()
        return len(self._bonds)
    
    def getAngles(self):
        
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
        if not self._hasAngle:
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
    def ndihedrals(self):
        if not self._hasDihedral:
            self.getDihedrals()
        return len(self._dihedrals)
    
    bonds = property(getBonds)
    angles = property(getAngles)
    dihedrals = property(getDihedrals)

 