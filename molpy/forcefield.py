# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-13
# version: 0.0.2

import molpy as mp
import numpy as np

class TypeBase:
    
    def __init__(self, id, name, **attr):
        self.id = id
        self.name = name
        self.update(attr)
        self._queryFunc = None
        
    def update(self, attr:dict):
        for k, v in attr.items():
            setattr(self, k, v)
            
    def __repr__(self):
        return f'< {self.__class__.__name__} {self.id}: {self.name} >'

    def getQueryFunc(self):
        return self._queryFunc

    def setQueryFunc(self, qf):
        self._queryFunc = qf

    QueryFunc = property(getQueryFunc, setQueryFunc)

class AtomType(TypeBase):
    
    def __init__(self, id, name, **attr:dict):
        super().__init__(id, name, **attr)

        
class BondType(TypeBase):
    
    def __init__(self, id, name, **attr:dict):
        super().__init__(id, name, **attr)


class PairType(TypeBase):

    def __init__(self, id, name, **attr:dict):
        super().__init__(id, name, **attr)

class TypeManagement:
    
    pass

class AtomTypeManagement(TypeManagement):
    
    def __init__(self):
        self._id2AtomType = {}  # id -> atomType
        self._name2AtomType = {}  # name -> atomType
        self._class2AtomTypes = {}  # class -> [atomType]
        self._nAtomTypes = 0
        
    def defAtomType(self, name, **attr):
        
        atomTypeId = self._nAtomTypes + 1  # start from 1
        at = AtomType(atomTypeId, name, **attr)
        
        if name in self._name2AtomType:
            raise KeyError(f'AtomTypeName {name} is already defined!')
        self._name2AtomType[name] = at
        
        if atomTypeId in self._id2AtomType:
            raise KeyError(f'AtomTypeId {atomTypeId} is already defined! This error is a bug of the atomTypeId management, please contact to developers.')
        self._id2AtomType[atomTypeId] = at
        
        # if atomClass in self._id2AtomType:
        #     self._class2AtomTypes[atomClass].add(at) 
        # else:
        #     self._class2AtomTypes[atomClass] = set()
            
        self._nAtomTypes += 1
        return at
    
    def getAtomTypeByName(self, name):
        return self._name2AtomType[name]
    
    def getAtomTypeById(self, id):
        return self._id2AtomType[id]
    
    def getAtomTypeByClass(self, class_):
        return list(self._class2AtomTypes[class_])

    
class BondTypeManagement(TypeManagement):
    
    def __init__(self):
        self._id2BondType = {}
        self._name2BondType = {}
        self._class2BondType = {}
        
        self._atomTypes2BondType = {}  # {atomType1: {atomType2: bondType}}
        
        self._nBondTypes = 0
        
    def defBondType(self, name, **attr):
        
        bondTypeId = self._nBondTypes + 1
        bt = BondType(bondTypeId, name, **attr)
        
        if name in self._name2BondType:
            raise KeyError(f'BondTypeName {name} is already defined!')
        
        if bondTypeId in self._id2BondType:
            raise KeyError(f'BondTypeId {bondTypeId} is already defined! This error is a bug of the atomTypeId management, please contact to developers.')

        self._id2BondType[bondTypeId] = bt
        
        # if bondClass in self._class2BondType:
        #     self._class2BondType[bondClass].add(bondClass)
        # else:
        #     self._class2BondType[bondClass] = set()
        
        # if itomType not in self._atomTypes2BondType:
        #     self._atomTypes2BondType[itomType] = {jtomType: bt}
        # else:
        #     self._atomTypes2BondType[itomType][jtomType] = bt
        
        # if jtomType not in self._atomTypes2BondType:
        #     self._atomTypes2BondType[jtomType] = {itomType: bt}
        # else:
        #     self._atomTypes2BondType[jtomType][itomType] = bt
        
        self._nBondTypes += 1
        return bt
    
    def getBondTypeByName(self, name):
        return self._name2BondType[name]
    
    def getBondTypeById(self, id):
        return self._id2BondType[id]
    
    def getBondTypeByClass(self, class_):
        return list(self._class2BondType[class_])
    
    def getBondTypeByAtomType(self, twoAtomTypes):
        itomType, jtomType = twoAtomTypes
        return self._atomTypes2BondType[itomType][jtomType]
        
class AngleTypeManagement(TypeManagement):
    pass

class DihedralTypeManagement(TypeManagement):
    pass

class ImproperTypeManagement(TypeManagement):
    pass

class PairTypeManagement(TypeManagement):
    
    def __init__(self):
        self._id2PairType = {}
        self._name2PairType = {}
        self._class2PairType = {}
        
        self._atomTypes2PairType = {}  # {atomType1: {atomType2: bondType}}
        
        self._nPairTypes = 0
        
    def defPairType(self, name, **attr):
        
        pairTypeId = self._nPairTypes + 1
        pt = PairType(pairTypeId, name, **attr)
        
        if name in self._name2PairType:
            raise KeyError(f'PairTypeName {name} is already defined!')
        
        if pairTypeId in self._id2PairType:
            raise KeyError(f'PairTypeId {pairTypeId} is already defined! This error is a bug of the atomTypeId management, please contact to developers.')

        self._id2PairType[pairTypeId] = pt
        self._nPairTypes += 1
        return pt
    
class ForceField(AtomTypeManagement, BondTypeManagement, PairTypeManagement):
    
    def __init__(self, unit='SI'):
        
        AtomTypeManagement.__init__(self)
        BondTypeManagement.__init__(self)
        PairTypeManagement.__init__(self)
        
        self._unit = unit

    def getQueryFuncs(self, which):
        if which == 'atomType':
            return {t: t.queryFunc for t in self._id2AtomType.values()}
        elif which == 'bondType':
            return {t: t.queryFunc for t in self._id2BondType.values()}
        elif which == 'pairType':
            return {t: t.queryFunc for t in self._id2PairType.values()}
    
    def queryAtomTypes(self, atoms):
        
        queryFuncs = self.getQueryFuncs('atomType')
        atomTypes = np.zeros(len(atoms), dtype=AtomType)
        atomArr = atoms.toStructuredArray()
        for atomType, queryFunc in queryFuncs.items():
            tmp = np.apply_along_axis(queryFunc, 0, atomArr)
            atomTypes[tmp] = atomType
        return atomTypes
        
    
    def queryBondTypes(self, atoms):
        
        bonds = atoms.getBondIdx()
        atomsOfBond = atoms.toStructuredArray()[bonds]
        bondTypes = np.zeros(len(atomsOfBond), dtype=BondType)
        queryFuncs = self.getQueryFuncs('bondType')
        for bondType, queryFunc in queryFuncs.items():
            tmp = np.apply_along_axis(queryFunc, 1, atomsOfBond)
    
            bondTypes[tmp] = bondType
        return bondTypes

    def queryPairTypes(self, atoms, box, rcutoff):
        
        positions = atoms.positions
        aq = mp.NeighborList(box, positions)
        pairs = np.array(list(aq.query(positions, dict(r_max=rcutoff))))
        pairIdx, distances = pairs[:, :2].astype(int), pairs[:, 2]
        atomArr = atoms.toStructuredArray()
        atomsOfPair = atomArr[pairIdx]
        pairTypes = np.zeros(len(pairs), dtype=PairType)

        queryFuncs = self.getQueryFuncs('pairType')
        for pairType, queryFunc in queryFuncs.items():
            tmp = np.apply_along_axis(queryFunc, 1, atomsOfPair)
            pairTypes[tmp] = pairType

        return pairType


        