# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-12
# version: 0.0.1

from molpy.io import Readers

class TestLammps:

    def test_lammps_io(self):

        reader = Readers['DataReaders']['lammps']('tests/test_io/data/lammps.data')
        data = reader.get_data()
        assert data

        