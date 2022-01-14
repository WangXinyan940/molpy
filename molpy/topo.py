# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from collections import defaultdict
from itertools import combinations

from .angle import Angles
from .bond import Bonds
from .dihedral import Dihedrals


class Topo:
    
    def __init__(self, connection=None, atoms=None):
        
        self.reset()
        
        if connection is not None:
            if isinstance(connection, dict):
                self.setConnection(connection)
            elif isinstance(connection, (list, tuple)):
                self.constructConnectionFromBonds(connection)
        
        if atoms is not None: 
            self.setAtoms(atoms)


    def reset(self):
        self._atoms = None
        self._bonds = None
        self._angles = None
        self._dihedrals = None
        self._hasBond = False
        self._hasAngle = False
        self._hasDihedral = False    
        self._hasAtom = False
        
    def setAtoms(self, atoms):
        
        atomArgType = getattr(atoms, '__class__', None)  # avoid to use :=
        if atomArgType:
            if atomArgType.__name__ == 'Atoms':
                self._atoms = atoms.getAtoms()
                
        self._hasAtom = True
                
        
    def setConnection(self, connection):
        self._connection = connection
        self.reset()
    
    def constructConnectionFromBonds(self, bonds):

        connection = defaultdict(list)
        for bond in bonds:
            connection[bond[0]].append(bond[1])
            connection[bond[1]].append(bond[0])
        self._connection = dict(connection)
        self.reset()
        
    def getBonds(self):
        
        if self._hasBond:
            return self._bonds
        
        topo = self._connection
        rawBonds = []
        for c, ps in topo.items():
            for p in ps:
                rawBonds.append([c, p])

        self._bonds = Bonds(rawBonds, self._atoms)
        return self._bonds
    
    def getAngles(self):
        
        if self._hasAngle:
            return self._angles

        topo = self._connection
        rawAngles = []
        for c, ps in topo.items():
            if len(ps) < 2:
                continue
            for (itom, ktom) in combinations(ps, 2):
                rawAngles.append([itom, c, ktom])
        self._angles = Angles(rawAngles, self._atoms)
        return self._angles
    
    def getDihedrals(self):
        
        if self._hasDihedral:
            return self._dihedrals
     
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
        self._dihedrals = Dihedrals(rawDihes, self._atoms)
        return self._dihedrals
    
    def getBondIdx(self):
        
        bonds = self.getBonds()
        return bonds.bondIdx
    
    def getAngleIdx(self):
        angles = self.getAngles()
        return angles.angleIdx
    
    def getDihedralIdx(self):
        dihe = self.getDihedrals()
        return dihe.dihedralIdx