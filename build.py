class A:
    
    def __init__(self):
        self.a = {}
        
    def __getitem__(self, key1):
        print(key1)
        
a = A()
a['test', 'test2']