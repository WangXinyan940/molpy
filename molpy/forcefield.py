# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-02-24
# version: 0.0.2

import xml.etree.ElementTree as ET

class AtomType:
    
    def __init__(self):
        
        self._properties = {}
        
    def __getitem__(self, o):
        return self._properties[o]
    
    def __setitem__(self, k, v):
        self._properties[k] = v

class AtomTypes:
    
    def __init__(self):
        
        self._atomTypes = []
        self._name2idx = {}
        self._class2idx = {}
        
    def getAtomTypeByName(self, keys):
        
        idx = [self._name2idx[key] for key in keys]
        types = [self._atomTypes[id] for id in idx]
        return types
    
    def getAtomTypeByClass(self, keys):
        
        idx = [self._class2idx[key] for key in keys]
        types = [self._atomTypes[id] for id in idx]
        return types
    
    def register(self, attrib):
        at = AtomType()
        for k, v in attrib.items():
            
            if k == 'name':
                self._name2idx[v] = at
            elif k == 'class':
                self._class2idx[v] = at
            else:
                at[k] = v
                
    def fromXML(self, section):
        
        for atomType in section:
            self.register(atomType.attrib)
            
    
class Forcefield:
        
    def __init__(self) -> None:
        pass

    def fromXML(self, filename):
                
        tree = ET.parse(filename)
        root = tree.getroot()
        assert root.tag == 'ForceField'
        
        for section in root:
            

        
            