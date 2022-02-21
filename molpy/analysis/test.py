from operator import add
from multiprocessing import Pool
import numpy as np
from time import sleep, time
import multiprocessing as mp
from freud import density
from freud.box import Box

# from molpy.analysis.utils import Accumulator

class Management:
    
    def __init__(self) -> None:
        self.np = 4
        self.pool = mp.Pool(self.np)
        
    def addTask1(self, func):
        
        task = self.pool.apply_async(func)
        return task
        
    def addTask2(self, class_, *args):
        
        def worker():
            ins = class_(*args)  
            print(f'init: {id(ins)}')
            return ins
        
        callback = lambda x: print(id(x))
            
        task = self.pool.apply_async(worker, callback=callback)
        
        return task
    
class Mock:
    
    def __init__(self, positions) -> None:
        
        self.positions = positions
        self.data = {}
        
    def start(self):
        
        self.rdfKernel = density.RDF(bins=200, r_max=4, r_min=0)
        self.rdfKernel.compute((Box.cube(10), self.positions))
        self.data['rdf'] = self.rdfKernel.rdf
        # self.accu = Accumulator(add, 'test')
        # self.accu(1)
        # self.accu(2)
        delattr(self, 'rdfKernel')
        
        return self
        
if __name__ == '__main__':
    
    ma = Management()
    
    mo = Mock(np.random.random((10, 3))*10)

    result = ma.addTask1(mo.start)
    ma.pool.close()
    ma.pool.join()
    mo_ = result.get()
    print(mo_.data['rdf'])
    