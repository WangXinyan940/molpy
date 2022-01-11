# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

# NOTE: experimental

import numpy as np
from numpy.lib import recfunctions as rfn

class Model:
    
    def __init__(self, n):
        super().__setattr__('_fields', {})
        self._n = n
        
    def __getattr__(self, field):
        return self._fields[field]
    
    def __setattr__(self, field, value):
        
        if field in self._fields:
            # TODO: validation
            self._fields[field] = value
        else:
            super().__setattr__(field, value)
            
    def check_alignment(self):
        field_lengths = np.array(map(len, self._fields.values()))
        if (field_lengths == self._n).all():
            return True
        return False
    
    @property    
    def dtype(self):
        tmp = []
        for k, v in self._fields.items():
            if isinstance(v, np.ndarray):
                if v.ndim == 1:
                    tmp.append( (k, v.dtype) ) 
                else:
                    tmp.append( (k, v.dtype, v.shape[1:]) )
            else:
                tmp.append( (k, type(v)) )
                
        return np.dtype(tmp)
    
    @property
    def fields(self):
        return self._fields
    
    @property
    def size(self):
        return self._n
        
    def __contains__(self, o):
        return o in self._fields.keys()
    
    def mergeFields(self, fields, newField, dtype):
        arrs = [self._fields[field] for field in fields]
        self._fields[newField] = np.concatenate(arrs)
        return self._fields[newField]
    
    def dropFields(self, fields):
        for field in fields:
            del self._fields[field]
    
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
            group_fields = {}
            for k, v in grouped_fields.items():
                group_fields[k] = v[i]
            n = len(group_fields[k])
            m = Model(n)
            m.appendFields(group_fields)
            models.append(m)
        return models
            
    def toStructuredArray(self):

        arrs = self._fields.values()
        lengths = map(len, arrs)
        maxLen = max(lengths)

        data = np.empty((maxLen, ), dtype=self.dtype)
        for key in self._fields.keys():
            data[key] = self._fields[key]

        return data
