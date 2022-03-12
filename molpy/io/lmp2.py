# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-12
# version: 0.0.1

__all__ = [
    'DataReader',
    'DataWriter',
    'DumpReader'
]

import numpy as np
from molpy.io.fileHandler import FileHandler

DECLEAR_TYPES = {
    'id': int,
    'mol': int,
    'type': int,
    'q': float,
    'x': float,
    'y': float,
    'z': float,
}

class DumpReader:
    
    def __init__(self, fpath:str):
        
        self.filepath = fpath
        self.filehandler = FileHandler(fpath)
        self.chunks = self.filehandler.readchunks('ITEM: TIMESTEP')
        
    def getFrame(self, index):
        
        chunk = self.chunks.getchunk(index)
        
        return DumpReader.parse(chunk)
        
    @staticmethod
    def parse(chunk:list[str]):
        
        data = {}
        
        data['timestep'] = int(chunk[1])
        data['natoms'] = int(chunk[3])
        xlo, xhi = [float(x) for x in chunk[5].split()]
        ylo, yhi = [float(x) for x in chunk[6].split()]
        zlo, zhi = [float(x) for x in chunk[7].split()]
        data['box'] = [xlo, xhi, ylo, yhi, zlo, zhi]
        
        header = chunk[8].split()[2:]
        
        m = map(lambda x: tuple(x.split()), chunk[9:])
        lm = list(m)
        atomArr = np.array(lm, dtype={'names': header, 'formats': [DECLEAR_TYPES[k] for k in header]})
        
        data['atomInfo'] = atomArr
        
        return data
            