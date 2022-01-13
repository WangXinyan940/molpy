# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-12
# version: 0.0.1

from molpy.forcefield import ForceField

class TestForceField:
    
    def test_init(self):
        ff = ForceField('test')
        ff.loadXmlFile('tests/mpidwater.xml')