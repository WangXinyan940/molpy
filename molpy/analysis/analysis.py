# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

from tqdm import tqdm
import numpy as np

class AnalysisQueue:
    
    def __init__(self):
        pass
    
    def one(self, path, do, checkFunc=None, elseFunc=None):
        
        if checkFunc(path):
            return True, do(path)
        else:
            return False, elseFunc(path)
        
    def map(self, paths, do, checkFunc=None, elseFunc=None):
        
        results = []
        errs = []
        
        for path in tqdm(paths):
            state, result = self.one(path, do, checkFunc, elseFunc)
            if state:
                results.append(result)
            else:
                errs.append(result)
            
        return results
    
class Analyzer:
    
    def __init__(self):
        pass
    
    def __post_init__(self):
        pass
    
    def check(self):
        raise NotImplementedError
    
    def before_analysis(self):
        pass
    
    def ensemble_average(self):
        pass
    
    def after_analysis(self):
        pass
        
    @staticmethod
    def save(fname, ):
        pass
