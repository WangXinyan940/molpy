# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.2

class System:
    
    def __init__(self):
        
        pass
        
    def getAtoms(self):
        return self.data.getAtoms()
    
    def getBonds(self):
        return self.topo.getBonds()
    
    def getAngles(self):
        return self.topo.getAngles()
        
    def getDihedral(self):
        return self.topo.getDihedral()
