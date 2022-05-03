# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-12
# version: 0.0.1

import pytest
from molpy.atoms import Atoms
from molpy.io.lmp import DumpReader, DataReader, DataWriter
from molpy.modeller.randomWalk import RandomWalkOnFcc
from molpy.system import System
import numpy.testing as npt
import numpy as np

class TestDump:
    
    @pytest.fixture(scope='class', name='dump')
    def test_init(self):
        
        dump = DumpReader('tests/data/linear.dump')
        yield dump
        
    def test_get_frame(self, dump):
        
        data = dump.getframe(2)
        assert data['timestep'] == 20
        assert data['natoms'] == 60
        atomInfo = data['atomInfo']
        npt.assert_allclose(np.asfarray(list(atomInfo[-1])), np.array('45 18 6 -11.8 2.37502 43.1304 46.726'.split(), dtype=float))
        
class TestData:
    
    @pytest.fixture(scope='class', name='data')
    def test_init_data(self):
        
        data = DataReader('tests/data/linear.data')
        yield data
        
    def test_parse_line(self):
        
        line = '\t60 Atom\n# comment'
        line = DataReader.parse_line(line)
        assert line == ('60', 'Atom')
        
        line = ''
        line = DataReader.parse_line(line)
        assert line != ['']
        
    def test_parse(self, data):
        
        data = data.getdata()
        atoms = data['Atoms']
        
        npt.assert_allclose(np.asfarray(list(atoms[-1])), np.array('60	33	6	-11.8000	40.2637	47.8022	 6.3059'.split(), dtype=float))
        
        bonds = data['Bonds']
        bond = bonds[0]
        assert bond[0] == 1
        assert bond[1] == 1
        assert bond[2] == 1
        assert bond[3] == 2
        
    @pytest.fixture(scope='class', name='system')
    def test_init_system(self):
        
        rw = RandomWalkOnFcc(10, 10, 10)
        positions, topo = rw.linear(10, )
        system = System('molpy IO test')
        atoms = Atoms.fromDict(dict(id=np.arange(len(positions), dtype=int)+1, position=positions, type=['c']*10, mol=[1]*10, q=[0.1]*10), dict(topo=topo, bondTypes=np.ones(len(topo), dtype=int)))
        # system.append(atoms)
        system.atomManager.atoms = atoms
        
        assert system.natoms == 10
        assert system.nbonds == 9
        assert system.nangles == 8
        assert system.ndihedrals == 7
        
        system.setBox(50, 50, 50)
        ff = system.forcefield
        
        ff.defAtomType('c', mass=1)
        ff.defBondType('cc', 'c', 'c')

        
        assert ff.natomTypes == 1
        assert ff.nbondTypes == 1
        
        yield system
        
    def test_write(self, system):
        
        d = DataWriter('test.data')
        d.write(system, isAngles=False, isDihedrals=False)
        data = DataReader('test.data').getdata()
        comment = data['comment']
        atoms = data['atoms']
        