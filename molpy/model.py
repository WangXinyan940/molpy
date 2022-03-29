# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from typing import Optional
import numpy as np
import warnings

class Model:
    
    def __init__(self, fields:dict=None):
        super().__setattr__('_fields', {})
        super().__setattr__('name', id(self))
        if fields is not None:
            if self.isAlign(fields):
                self._fields.update(fields)
            
    @staticmethod
    def fromModel(model):
        return Model(model.fields)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name} with len {len(self)}>'
    
    def __len__(self):
        if not self.isAlign():
            warnings.warn('not align')
        else:
            if len(self._fields.values()) == 0:
                return 0
            return len(next(iter(self._fields.values())))
        
    @property
    def n(self):
        return self.__len__()
    
    @property
    def nfields(self):
        return len(self._fields.values())
        
    def __getattr__(self, field):
        ans = self._fields.get(field, 'undifined')
        if ans == 'undifined':
            return super().__getattribute__(field)
        else:
            return ans
    
    def __setattr__(self, field, value):
        
        if field in self._fields:
            # TODO: validation
            self._fields[field] = value
        else:
            super().__setattr__(field, value)
            
    def isAlign(self, fields:Optional[dict]=None):
        
        if fields is None:
            fields = self._fields.values()
                
        field_lengths = np.asarray(tuple(map(len, fields)))
        if (field_lengths == 0).all():
            return True
        elif (field_lengths == 0).any():
            return False
         
        field_lengths -= np.max(field_lengths)
        field_lengths = field_lengths.astype(np.bool_)
        if ~field_lengths.all():
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
    
    def mergeFields(self, fields, newField):
        arrs = [self._fields[field] for field in fields]
        self._fields[newField] = np.vstack(arrs).T
        return self._fields[newField]
    
    def dropFields(self, fields):
        for field in fields:
            del self._fields[field]
    
    def appendFields(self, fields:dict):
        
        for field in fields.values():
            if hasattr(field, 'shape') and (field.shape[0] != self._n):
                raise ValueError(f'append field {field}\'s shape {field.shape} not match {self._n}')
            elif isinstance(field, (list, tuple)) and (len(field) != self._n):
                raise ValueError(f'append field {field}\'s shape {len(field)} not match {self._n}')
        
        self._fields.update(fields)
            
    def __getiems__(self, o):
        
        if isinstance(o, str):
            return self._fields[o]
        
    def __contains__(self, o):
        return o in self.fields
        
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

    def fromStructuredArray(self, arr):
        
        arrDict = {}
        for field in arr.dtype.fields:
            arrDict[field] = arr[field]
        self.appendFields(arrDict)