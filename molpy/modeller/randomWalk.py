from molpy_cpp.randomWalk import SimpleRW as SimpleRW_cpp

class SimpleRW:
    
    def __init__(self):
        
        self._workload = SimpleRW_cpp()
        
    def walk(self, lchain, nchain):
        
        self._workload.walk(lchain, nchain)
        
    @property
    def positions(self):
        
        return self._workload.getPositions()
    
    @property
    def links(self):
        
        return self._workload.getLinks()
    
    