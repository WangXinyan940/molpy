# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from itertools import combinations
from .bond import Bonds
from .angle import Angles
from .dihedral import Dihedrals
from collections import defaultdict

class Topo:
    
    def __init__(self, connection=None):
        
        if connection is not None:
            self._connection = connection
    
    def setAtomInstances(self, atoms):
        self._atoms = atoms
    
    @property
    def atoms(self):
        return getattr(self, '_atoms', None)
        
    def setConnection(self, connection):
        self._connection = connection
    
    def constructConnectionFromBonds(self, bonds):
        self._bonds = bonds
        self._hasBonds = True
        connection = defaultdict(list)
        for bond in bonds:
            connection[bond[0]].append(bond[1])
            connection[bond[1]].append(bond[0])
        self._connection = dict(connection)
        
    def getBonds(self):
        topo = self._connection
        rawBonds = []
        for c, ps in topo.items():
            for p in ps:
                rawBonds.append([c, p])
        return Bonds(rawBonds, self.atoms)
    
    def getAngles(self):

        topo = self._connection
        rawAngles = []
        for c, ps in topo.items():
            if len(ps) < 2:
                continue
            for (itom, ktom) in combinations(ps, 2):
                rawAngles.append([itom, c, ktom])

        return Angles(rawAngles, self.atoms)
    
    def getDihedrals(self):
     
        topo = self._connection
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
        return Dihedrals(rawDihes, self.atoms)