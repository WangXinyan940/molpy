# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

from typing import Any, Callable, Iterable, Literal
from tqdm import tqdm
import numpy as np
import multiprocessing as mp

class Analyzer:
    
    def __init__(self, name):
        """ initialize an analyzer. generally including setting the path of data, loading data or invoking __post_init__
        """
        self._name = name
        self._data = {}
    
    @property
    def name(self):
        return self._name if getattr(self, '_name') else id(self)
    
    @property
    def data(self):
        return self._data
    
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
        
        if getattr(analyzer, 'start', None) is None:
            raise AttributeError
        
        task_flag = self.pool.apply_async(analyzer.start, args, kwargs, callback, err_callback)
        self.tasks[analyzer.name] = (analyzer, task_flag)
        
    def retrive(self, block=True):

        analyzers = []
        tasks = self.tasks.keys()
        if block:
            # before join(), must close()
            # and no more tasks can be added
            self.pool.close()
            self.pool.join()
            
        for taskname in tasks:
            ana, task_flag = self.tasks[taskname]
            if task_flag.ready():
                print(f'{taskname} ready')
                analyzers.append(ana)
            else:
                print(f'{taskname} is not ready')
        return analyzers
        
    
