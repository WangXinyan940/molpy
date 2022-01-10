# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.1

# NOTE: experimental

import numpy as np

class ModelMetaclass(type):
    
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        fields = dict()
        for k, v in attrs.items():
            if isinstance(v, np.ndarray):
                print('Found mapping: %s ==> %s' % (k, v))
                fields[k] = v
        for k in fields.keys():
            attrs.pop(k)
        attrs['__fields__'] = fields
        attrs['__modelType__'] = name
        return type.__new__(cls, name, bases, attrs)
    
class Model(metaclass=ModelMetaclass):
    
    def __init__(self, **fields) -> None:
        print(fields)
        pass
    
class Molecule(Model):
    pass
    
m = Molecule(id=np.array([1,2,3]), position=np.arange(9).reshape((3,3)))
print(m)