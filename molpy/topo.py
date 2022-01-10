# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from itertools import combinations
from .bond import Bonds
from .angle import Angles
from .dihedral import Dihedrals

class Topo:
    
    def __init__(self, atoms):
        self._atoms = atoms
        
    @property
    def atoms(self):
        return self._atoms
    
    def fromBondList(self, bonds, bondTypes):
        self._bonds = bonds
        self._bondTypes = bondTypes
        self._hasBonds = True
        # construct _topo
        
    def getBonds(self):
        if not self._hasBonds:
            topo = self._topo
            rawBonds = []
            for c, ps in topo.items():
                for p in ps:
                    rawBonds.append([c, p])
            self._bonds = rawBonds
        return Bonds(self._bonds, self._atoms)
    
    def getAngles(self):
        if not self._angles:
            topo = self._topo
            rawAngles = []
            for c, ps in topo.items():
                if len(ps) < 2:
                    continue
                for (itom, ktom) in combinations(ps, 2):
                    rawAngles.append([itom, c, ktom])
            self._angles = rawAngles
        return Angles(self._angles, self._atoms)
    
    def getDihedrals(self):
        if not self._dihedrals:
            topo = self._topo
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
            self._dihedrals = rawDihes
        return Dihedrals(self._dihedrals, self._atoms)