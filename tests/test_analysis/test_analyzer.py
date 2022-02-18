# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-02-18
# version: 0.0.1

import numpy as np
from time import time, sleep
from molpy.analysis import Analyzer, AnalysisManagement

class MockAnalyzer(Analyzer):
    
    def __init__(self, name, path):
        self._name = name
        self.path = path
    
    def start(self):
        sleep(3)

class TestAnalysisQueue:
    
    def test_init_am(self):
        am = AnalysisManagement()
        for i in range(5):
            an = MockAnalyzer(f'a{i}', 'path{i}')
            am.addTask(an)
        analyzers = am.retrive()
        assert len(analyzers) != 5
        sleep(5)
        analyzers = am.retrive()
        assert len(analyzers) == 5
