# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.2

import numpy as np

class ModelMetaClass:
    pass


class Model:
    
    def __init__(self, size: int, fields: list=None, copy=None, **data: dict) -> None:
        
        if fields is not None:
            
            fields = np.dtype(fields)
            dtype = [(f, d[0]) for f, d in fields.fields.items()]
            data = {k: np.array(v) for k, v in data.items()}
            dtype.extend([(f, d.dtype, d.shape[1:]) for f, d in data.items()])
            super().__setattr__('_data', np.zeros(size, dtype=dtype))
            for k, v in data.items():
                self.data[k] = v
            super().__setattr__('_size', size)
            
        # tmp = np.zeros(self.natoms, dtype=object)
        # for i in range(self.natoms):
        #     tmp[i] = self.data[i]
        # return tmp
            
        if fields is None and copy is not None:
            super().__setattr__('_data', copy)

    def __getattr__(self, name):
        return self.data[name]
    
    def __setattr__(self, name, value):
        
        if name in self.data.dtype.names:
            self.data[name] = value
        else:
            super().__setattr__(name, value)
            
    @property
    def dtype(self):
        return self.data.dtype
    
    @property
    def data(self):
        return self._data
    
            
if __name__ == '__main__':
    model = Model(
        5,
        [("id", int), ("position", float, (3,))],
        group=[1, 2, 3, 4, 5],
        vel=np.random.random((5, 3)),
    )
    model.id = np.arange(5)