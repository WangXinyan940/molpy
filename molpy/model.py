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
                
        return tmp
    
    @property
    def fields(self):
        return self._fields
    
    def mergeFields(self, fields, newField, dtype):
        pass
    
    def dropFields(self, fields):
        pass
    
    def appendField(self, field, value):
        pass
    