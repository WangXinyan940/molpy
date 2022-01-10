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
    
    def __init__(self, filename):
        self.filename = filename
    
    def parse(self, ):
        raise NotImplementedError("Override this in each subclass")
    
    def pre_parse(self, ):
        raise NotImplementedError("Override this in each subclass")
    
    
class WriteBase:
    
    pass
