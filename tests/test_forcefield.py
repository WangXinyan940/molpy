# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-05
# version: 0.0.2

import pytest

from molpy.forcefield import AtomType, AtomTypes, BondType, BondTypes, Forcefield

class TestAtomType:
    
    @pytest.fixture(scope='class', name='at')
    def test_init(self):
        at1 = AtomType('380')
        at1.properties.update(dict(class_='OW', element='O', mass='15.999'))
        yield at1

    def test_match(self, at):
        assert at.match('380')
        assert at.match('OW')
        assert at.match(at)
        
class TestAtomTypes:
    
    @pytest.fixture(scope='class', name='atomTypes')
    def test_init(self):
        yield AtomTypes()
        
    def test_defAtomType(self, atomTypes):
        at1 = AtomType('380')
        at1.properties.update(dict(class_='OW', element='O', mass='15.999'))
        at2 = AtomType('381')
        at2.properties.update(dict(class_='HW', element='H', mass='1.008'))
        atomTypes[at1.name] = at1
        atomTypes[at2.name] = at2
        assert atomTypes['380'] == at1
        assert atomTypes['381'] == at2
        assert atomTypes['380'].properties['class_'] == 'OW'
        assert atomTypes['381'].properties['class_'] == 'HW'
        
    def test_getAtomTypeByClass(self, atomTypes):

        assert atomTypes.getAtomTypeByClass('OW') == [atomTypes['380']]
        assert atomTypes.getAtomTypeByClass('HW') == [atomTypes['381']]
        
class TestBondType:
    
    @pytest.fixture(scope='class', name='bondType')
    def test_init(self):
        pass

class TestBondTypes:
    
    @pytest.fixture(scope='class', name='bondTypes')
    def test_init_(self):
        return BondTypes()
    
    def test_defBond(self, bondTypes):
        
        at1 = AtomType('380')
        at1.properties.update(dict(class_='OW', element='O', mass='15.999'))
        at2 = AtomType('381')
        at2.properties.update(dict(class_='HW', element='H', mass='1.008'))
        bondTypes[at1, at2] = BondType('HarmonicBondForce')
        bondTypes[at1, at2].properties.update(dict(class_='HarmonicBondForce', k=0.1, r0=1.5))
        
        assert bondTypes['OW', 'HW'].properties['r0'] == 1.5
        assert bondTypes['381', '380'].properties['r0'] == 1.5
        assert bondTypes[at1, at2].properties['r0'] == 1.5
        

class TestForceField:
    
    @pytest.fixture(scope='class', name='ff')
    def test_init_(self):
        ff = Forcefield()
        return ff
    
    def test_defAtomType(self, ff):
        ff.defAtomType('380', class_='OW', element='O', mass='15.999')
        ff.defAtomType('381', class_='HW', element='H', mass='1.008')
        assert ff.atomTypes['380'].properties['mass'] == '15.999'
        assert ff.atomTypes['380'].properties['element'] == 'O'
        assert ff.atomTypes['380'].properties['class_'] == 'OW'
        
    def test_defBondType(self, ff):
        ff.defBondType('HarmonicBondForce', class1='OW', class2='HW', properties={'r0':1.5})
        assert ff.nAtomTypes == 2
        assert ff.bondTypes['OW', 'HW'].properties['r0'] == 1.5
        assert ff.bondTypes['380', '381'].properties['r0'] == 1.5
        
    def test_fromXML(self, ff):
        
        ff.fromXML('tests/data/forcefield.xml')
        assert ff.atomTypes['380'].properties['mass'] == '15.999'