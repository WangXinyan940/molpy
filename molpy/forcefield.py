# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-05
# version: 0.0.2

from xml.etree import ElementTree as ET

class AtomTypes(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        
    def getAtomTypeByClass(self, className):
        return [at for at in self.values() if at.properties['class_'] == className]
    
    @property
    def n(self):
        return len(self)
    
    def getAtomTypeByName(self, name):
        return self[name]
    
    def getAll(self):
        return list(self.values())
    
    def __len__(self) -> int:
        return super().__len__()
    
    def __iter__(self):
        return list(self.values()).__iter__()
    
        
class BondTypes:
    
    def __init__(self) -> None:
        super().__setattr__('bondMatrix', {})
        self.nbondTypes = 0
        
    def __getitem__(self, key):
        
        tag1, tag2 = key
        for at1 in self.bondMatrix:
            if at1.match(tag1):
                for at2 in self.bondMatrix[at1]:
                    if at2.match(tag2):
                        return self.bondMatrix[at1][at2]
        return None
        
    def __setitem__(self, keys, bondType) -> None:
        atomType1, atomType2 = keys
        self.bondMatrix.setdefault(atomType1, {})[atomType2] = bondType
        self.bondMatrix.setdefault(atomType2, {})[atomType1] = bondType
        self.nbondTypes += 1
        
    def getAll(self):
        tmpSet = set()
        for at1 in self.bondMatrix:
            for at2 in self.bondMatrix[at1]:
                tmpSet.add(self.bondMatrix[at1][at2])
        return list(tmpSet)
    
    def __len__(self):
        return self.nbondTypes
    
    def __iter__(self):
        return self.getAll().__iter__()
        
class BaseType:
    
    def __init__(self, name):
        self.name = name
        
    @property
    def properties(self):
        return self.__dict__
        
    def match(self):
        raise NotImplementedError
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, o):
        return True if hash(self) == hash(o) else False        
        
class AtomType(BaseType):
    
    typeId = 1
    
    def __init__(self, name) -> None:
        super().__init__(name)
        AtomType.typeId += 1
        
    def match(self, tag):
        
        if tag == self.properties.get('name', None) or tag == self.properties.get('class_', None) or tag == self:
            return True
        return False
        
class BondType(BaseType):
    
    typeId = 1
    
    def __init__(self, name) -> None:
        super().__init__(name)
        BondType.typeId += 1

class Forcefield:
    
    def __init__(self):
        
        self.atomTypes = AtomTypes()
        self.bondTypes = BondTypes()
        
    @property
    def nAtomTypes(self):
        return self.atomTypes.n
    
    @property
    def nBondTypes(self):
        return self.bondTypes.n
        
    def defAtomType(self, name, **properties):
        
        if name in self.atomTypes:
            at = self.atomTypes[name]
        else:
            at = AtomType(name)
            self.atomTypes[name] = at
        at.properties.update(properties)
        
    def defBondType(self, name, type1=None, type2=None, class1=None, class2=None, **properties):
        

        if type1 and type2:
            at1 = self.atomTypes[type1]
            at2 = self.atomTypes[type2]
            if self.bondTypes[type1, type2]:
                bt = self.bondTypes[type1, type2]
            else:
                bt = BondType(name)
                self.bondTypes[at1, at2] = bt
            bt.properties.update(properties)
            
        elif class1 and class2:
            
            at1s = self.atomTypes.getAtomTypeByClass(class1)
            at2s = self.atomTypes.getAtomTypeByClass(class2)
            
            for at1 in at1s:
                for at2 in at2s:
                    if self.bondTypes[type1, type2]:
                        bt = self.bondTypes[type1, type2]
                    else:
                        bt = BondType(name)
                        self.bondTypes[at1, at2] = bt
                    bt.properties.update(properties)
        
        
    def fromXML(self, filename):
        
        tree = ET.parse(filename)
        root = tree.getroot()
        
        for at in root.findall('AtomTypes/Type'):
            name = at.attrib.pop('name')
            self.defAtomType(name, **at.attrib)
            
        for bt in root.findall('BondTypes/Type'):
            name = bt.attrib.pop('name')
            self.defBondType(name, **bt.attrib)
            
    @property
    def natomTypes(self):
        return len(self.atomTypes)
    
    @property
    def nbondTypes(self):
        return len(self.bondTypes)
        
    @property
    def nangleTypes(self):
        return len(self.nangleTypes)
    
    @property
    def ndihedralTypes(self):
        return len(self.ndihedralTypes)
        