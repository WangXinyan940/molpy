# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

from typing import Any, Callable, Iterable, Literal
from tqdm import tqdm
import numpy as np
import multiprocessing as mp

class Analyzer:
    
    def __init__(self):
        """ initialize an analyzer. generally including setting the path of data, loading data or invoking __post_init__
        """
        pass
    
    @property
    def name(self):
        return self._name if getattr(self, '_name') else id(self)
    
    def __post_init__(self):
        """ initialize computing kernel
        """
        raise NotImplementedError
    
    def open(self):
        """ how to load data
        """
        raise NotImplementedError
    
    def before(self):
        """ not decide yet
        """
        raise NotImplementedError
    
    def start(self):
        """ start to analysis each frame
        """
        raise NotImplementedError
    
    def after(self):
        """ dump data etc.
        """
        raise NotImplementedError
    
    def one(self):
        """how to compute one frame
        """
        raise NotImplementedError
        
    def dump(self):
        pass


class AnalysisManagement:
    
    def __init__(self, np=mp.cpu_count(), timeout=None):
        
        self.np = np
        self.pool = mp.Pool(self.np)
        self.tasks = {}
        self.timeout = float(timeout) if timeout is not None else timeout
        
    def __del__(self):
        self.pool.terminate()
        print('exit safely')
        
    def addTask(self, analyzer, args:Iterable=(), kwargs:dict={}, callback:Callable[[Any],Any]=None, err_callback:Callable[[Exception],Any]=None):
        task = self.pool.apply_async(analyzer.start, args, kwargs, callback, err_callback)
        self.tasks[analyzer.name] = task
        
    def retrive(self):

        analyzers = []
        tasks = list(self.tasks.keys())
        for taskname in tasks:
            task = self.tasks[taskname]
            if task.ready():
                print(f'{taskname} ready')
                self.tasks.pop(taskname)
                analyzer = task.get()
                analyzers.append(analyzer)
            else:
                print(f'{taskname} is not ready')
        return analyzers
        
    
