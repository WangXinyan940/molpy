# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

# NOTE: experimental

import numpy as np

class Model:
    
    def __init__(self):
        super().__setattr__('_fields', {})
        
    def __getattr__(self, field):
        return self._fields[field]
    
    def __setattr__(self, field, value):
        
        if field in self._fields:
            # TODO: validation
            self._fields = value
        else:
            super().__setattr__(field, value)
    
    @property    
    def dtype(self):
        tmp = []
        for k, v in self._fields.items():
            if v.ndim == 1:
                tmp.append( (k, v.dtype) ) 
            else:
                tmp.append( (k, v.dtype, v.shape[1:]) )
                
        return np.dtype(tmp)
    
    @property
    def fields(self):
        return self._fields
    
    def __contains__(self, o):
        return o in self._fields.keys()
    
    def mergeFields(self, fields, newField, dtype):
        pass
    
    def dropFields(self, fields):
        pass
    
    def appendFields(self, fields:dict):
        # TODO: validation
        self._fields.update(fields)
            
    def __getiems__(self, o):
        
        if isinstance(o, str):
            return self._fields[o]
        
    def groupby(self, field):
        
        tmp = self._fields[field].argsort()
        index = np.unique(self._fields[field], return_index=True)[1][1:]
        
        grouped_fields = {}
        
        for k, v in self._fields.items():
            grouped_fields[k] = np.split(tmp, index)
        
        models = []
        for i in range(len(index)+1):
            m = Model()
            group_fields = {}
            for k, v in grouped_fields.items():
                group_fields[k] = v[i]
            m.appendFields(group_fields)
            models.append(m)
        return models
            
        