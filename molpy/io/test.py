
class A(type):
    
    def __new__(cls, name, base, attr):
        return super().__new__(cls, name, base, attr)
    
class AA(metaclass=A):
    
    def __init__(self):
        pass
    
aa = AA()