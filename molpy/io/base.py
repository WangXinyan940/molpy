# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from molpy.io import formats, parsers

class IOMetaClass(type):
    
    def __new__(cls, name, base, attrs):
        newCls = type.__new__(cls, name, base, attrs)
        try:
            fmt = attrs['format']
        except KeyError:
            pass
        else:
            formats.extend(fmt)
            parsers.append(newCls)
        return newCls
        
class ReaderBase(metaclass=IOMetaClass):
    
    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.kwargs = kwargs
        self.pre_parse()
    
    def parse(self, ):
        raise NotImplementedError("Override this in each subclass")
    
    def pre_parse(self, ):
        raise NotImplementedError("Override this in each subclass")
    
    
class WriterBase(metaclass=IOMetaClass):
    
    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.kwargs = kwargs


class FrameMetaInfo:
    
    def __init__(self):
        self.start_lino = []
        self.start_byte = []
        self.timesteps = []
        self.natoms = []
        self.box = []
        self.header = []
    
    @property
    def nframes(self):
        return len(self.timesteps)
    
class ReaderTrajBase(ReaderBase):
    
    def __init__(self, filename, **kwargs):
        self.frameMetaInfo = FrameMetaInfo()
        self.index = 0
        super().__init__(filename)
        
    @property
    def start_lino(self):
        return self.frameMetaInfo.start_lino[self.index]
    
    @property
    def start_byte(self):
        return self.frameMetaInfo.start_byte[self.index]
        
    @property
    def timesteps(self):
        return self.timesteps[self.index]
    
    @property
    def natoms(self):
        return self.frameMetaInfo.natoms[self.index]
    
    @property
    def box(self):
        return self.frameMetaInfo.box[self.index]
    
    @property
    def header(self):
        return self.frameMetaInfo.header
    
    @property
    def nframes(self):
        return self.frameMetaInfo.nframes