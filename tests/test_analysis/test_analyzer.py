# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-02-21
# version: 0.0.1

from molpy.analysis.analysis import Analyzer
from time import sleep

class MockAnalyzer(Analyzer):
    
    def __init__(self, name):
        super().__init__(name)
        self.data = {}
        
    def start(self, loop, sleeptime):

        
        for i in range(loop):
            sleep(sleeptime)
            
        self.loop = loop
        self.data['sleeptime'] = sleeptime
        
    def __call__(self, *args, **kwargs):
        self.start(*args, **kwargs)
        
class TestAnalyzer:
    
    def test_init(self):

        mock = MockAnalyzer('test')
        mock.start(3, 0.3)
        mock(3, 0.2)
        assert mock.loop == 3
        assert mock.data['sleeptime'] == 0.2
        
    
    