# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-04
# version: 0.0.2

import numpy as np
from .atom import Atom
from .bond import Bond
import numpy.lib.recfunctions as rfn

class Molecule:
    """atom->residue->segment->molecule
    """
    def __init__(self, name, natoms: int = None, fields: tuple = None, bondData=None):

        self._name = name
        self._natoms = natoms

        self.atomData = self.initAtomData(natoms, fields)
        self.bondData = self.initBondData(bondData)
        
    def __getattr__(self, name:str):
        if name in self.atomData.dtype.names:
            return self.atomData[name]
        else:
            raise AttributeError

    @property
    def natoms(self):
        if self._natoms is None:
            raise ValueError
        else:
            return self._natoms

    def initAtomData(self, natoms=None, fields=None):
        fields = list(fields)
        if natoms is None:
            return None
        else:
            sa = np.zeros((natoms,), dtype=fields)
            return np.rec.array(sa)

    def initBondData(self, bondData):

        return np.array(bondData)

    def getAtom(self, i):
        atom = Atom()
        atom.atomData = self.atomData[i]
        return atom

    def getAtoms(self, indices):

        return list(map(self.getAtom, self.atomData[indices]))

    def getAtomData(self, fields):
        return self.atomData[fields]

    def setAtomData(self, fields, dtype, values):
        rfn.append_fields(self.atomData, fields, dtypes=dtype)
        self.atomData[fields] = values

    def getBond(self, i, j):
        itom = self.getAtom(i)
        jtom = self.getAtom(j)
        return Bond(itom, jtom)

    def getBonds(self):
        return list(map(self.getBond, self.bondData))

    def __getitem__(self, o):
        return self.atomData[o]
        
    def getBondedAtom(self, i):
        bondData = self.bondData
        m1 = bondData[:, 0][bondData==i]
        bondedAtom = bondData[m1][:, 1]
        tmp = []
        # tmp.extend(map(partial(self.getBond, i=i), bondedAtom))
        tmp.extend(bondedAtom)
        m2 = bondedAtom[:, 1][bondData==i]
        bondedAtom = bondData[m2][:, 0]
        # tmp.extend(map(partial(self.getBond, i=i), bondedAtom))
        tmp.extend(bondedAtom)
        return tmp
    
m = Molecule('C6', 6, (('name', str), ('position', float, (3, ))), ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)))
