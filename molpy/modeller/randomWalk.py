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
    
    @property
    def lastPositions(self):
        
        return self._workload.getLastWalk()
    
    @property
    def lastLinks(self):
        
        return self._workload.getLastLinks()
    
    def walkOnce(self, lchain):
        
        return self._workload.walkOnce(lchain)
    
    def walkOnceFrom(self, start, lchain):
        
        return self._workload.walkOnceFrom(start, lchain)
    
    def findStart(self):
        
        return self._workload.findStart()
    
    def reset(self):
        
        return self._workload.reset()