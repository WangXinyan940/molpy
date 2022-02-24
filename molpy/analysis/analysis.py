# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

from functools import partial
from multiprocessing.pool import AsyncResult
from typing import Any, Callable, Iterable, Literal, Mapping
import multiprocessing as mp


class Analyzer:
    
    def __init__(self, name):
        """ initialize an analyzer. generally including setting the path of data, loading data or invoking __post_init__
        """
        self._name = name
        self._kernel = {}
    
    @property
    def name(self):
        return self._name if getattr(self, '_name') else id(self)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError
    
    def __eq__(self, o):
        return id(self) == id(o)
    
    def __hash__(self) -> int:
        return id(self)
    
    def defKernel(self, name, kernel, ):
        
        self._kernel[name] = kernel
        setattr(self, name, kernel)
        return kernel
    
    def delKernel(self, name=None):
        if name is None:
            for key in self._kernel:
                delattr(self, key)
            delattr(self, '_kernel')
        else:
            delattr(self, name)
            self._kernel.pop(name)


class AnalysisTaskManagement:
    
    def __init__(self, nprocessors=mp.cpu_count(), timeout=None):
        
        self.nprocessors = nprocessors
        self._pool = None
        self.tasks = {}
        self.lauch()
        
    def lauch(self, nprocessors=None):
        
        if nprocessors is None:
            nprocessors = self.nprocessors
        self._pool = mp.Pool(nprocessors)
        
    def terminate(self):
        self._pool.terminate()
        
    def __del__(self):
        self.terminate()
        
    def newTask(self, analyzer:Analyzer, args:Iterable=(), kwargs:Mapping={}, callback:Callable[[Analyzer], None]=None, err_callback:Callable[[BaseException], None]=None) -> AsyncResult:
        
        task = self._pool.apply_async(analyzer, args, kwargs, callback, err_callback) 
        self.tasks[analyzer.name] = task
        return task
    
    def getTaskConstructor(self, analyzer:Analyzer, callback:Callable[[Analyzer], None]=None, err_callback:Callable[[BaseException], None]=None) -> Callable[[Iterable, Mapping], Callable]:
        
        return partial(self.newTask, analyzer, callback=callback, err_callback=err_callback)
    
    def retrive(self, block=True) -> Mapping:
        
        if block:
            self._pool.close()
            self._pool.join()
            
        tmp = {}
        task_list = [name for name in self.tasks.keys()]
        for taskName in task_list:
            task = self.tasks[taskName]
            if task.ready():
                tmp[taskName] = task.get()
                self.tasks.pop(taskName)
            else:
                pass
        
        return tmp
    
    
    