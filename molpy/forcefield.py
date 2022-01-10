# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-06
# version: 0.0.2

import numpy as np


class TypeBase:
    
    def __new__(cls, name, matchFunc, *args, **kwargs):
        
        if name in cls.types:
            return cls.types[name]
        else:
            ins = super().__new__(cls)
            cls.types[name] = ins
            cls.typeID += 1
            ins.typeID = cls.typeID
            ins.itemType = cls.__name__[0].lower() + cls.__name__[1:]
            return ins
        
    def __init__(self, name, matchFunc, **attr):
        
        self.name = name
        self._match = matchFunc
        
    def match(self, item):
            return self._match(item)
    
class AtomType(TypeBase):
    
    typeID = 0
    types = {}
    
class BondType(TypeBase):
    
    typeID = 0
    types = {}
    
class AngleType(TypeBase):
    
    typeID = 0
    types = {}
    
class DihedralType(TypeBase):
    
    typeID = 0
    types = {}
    

class ForceField:
    
    def __init__(self, name, unit='SI') -> None:
        self.name = name
        self._templates = {}
        self._atomTypes = {}
        self._bondTypes = {}
        self._angleTypes = {}
        self._dihedralTypes = {}
        
    @property
    def natomTypes(self):
        return len(self._atomTypes)
    
    @property
    def nbondTypes(self):
        return len(self._bondTypes)
    
    @property
    def nangleTypes(self):
        return len(self._angleTypes)
    
    @property
    def ndihedralTypes(self):
        return len(self._dihedralTypes)
    
    @property
    def ntemplates(self):
        return len(self._templates)
        
    def defAtomType(self, atomName, **attr):

        if atomName in self._angleTypes:
            raise KeyError(f'atomType {atomName} has been defined')
        
        self._atomTypes[atomName] = AtomType(atomName, **attr)
        return self._atomTypes[atomName]
        
    def defBondType(self, bondName, **attr):

        if bondName in self._bondTypes:
            raise KeyError(f'bondType {bondName} has been defined')
        self._bondTypes[bondName] = BondType(bondName, **attr)
        return self._bondTypes[bondName]
        
    def defAngleType(self, angleName, **attr):

        if angleName in self._angleTypes:
            raise KeyError(f'angleType {angleName} has been defined')
        self._angleTypes[angleName] = AngleType(angleName, **attr)
        return self._angleTypes[angleName]
        
    def defDihedralType(self, dihedralName, **attr):
        
        if dihedralName in self._dihedralTypes:
            raise KeyError(f'dihedralType {dihedralName} has been defined')
        self._dihedralTypes[dihedralName] = DihedralType(dihedralName, **attr)
        return self._dihedralTypes[dihedralName]
    
    def getAtomType(self, name):
        atomType = self._atomTypes.get(name, None)
        if atomType is None:
            raise KeyError(f'atomType {name} is not defined yet')
        return atomType
        
    def typify(self, atoms, isBond=True, isAngle=True, isDihedral=True):
        """Add information from the forcefield to the group
        """
        # typify atom from forcefield.atomType
        perAtomData = atoms.data
        topo = atoms.topo
        
        self.typifyAtom(perAtomData)
        
        # typify bond from forcefield.bondType
        if isBond:
            for bond in atoms.bonds:
                self.typifyBond(bond)
            
        # typify angle from forcefield.angleType 
        if isAngle:
            for angle in atoms.angles:
                self.typifyAngle(angle)

        # typify dihedral from forcefield.dihedralType 
        if isDihedral:
            for dihedral in atoms.dihedrals:
                self.typifyDihedral(dihedral)
            
    def typifyAtom(self, atoms):

        atomTypeArray = np.zeros(len(atoms), dtype=object)
        for atomType in self.atomTypes.values():
            # matchFun = np.vectorize(atomType.match)
            matchFun = atomType.match
            mask = matchFun(atoms)
            atomTypeArray[mask] = atomType
        return atomTypeArray
    
    def typifyBond(self, topo):
        
        bonds = topo.bonds
        
                
    @property
    def atomTypes(self):
        return self._atomTypes
    
    @property
    def bondTypes(self):
        return self._bondTypes
    
    @property
    def angleTypes(self):
        return self._angleTypes
    
    @property
    def dihedralTypes(self):
        return self._dihedralTypes
    