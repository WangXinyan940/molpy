# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

from logging import warning
from typing import List, Literal, Optional
from molpy.bond import Bond
from molpy.angle import Angle
from molpy.dihedral import Dihedral
from molpy.neighborlist import NeighborList
from molpy.utils import fromStructToDict
from .topo import Topo
from .model import Graph
from .atom import Atom
import numpy as np


class Atoms(Graph):
    def __init__(self, name=None):
        super().__init__(name)
        
    @classmethod
    def fromDict(cls, nodes, edges, globals, topo, name=None):
        atoms = cls()
        atoms.nodes = nodes
        atoms.edges = edges
        atoms.globals = globals
        atoms.topo.setTopo(topo)
        return atoms

    def __iter__(self):
        return iter(self.atoms)

    @property
    def atoms(self):
        return self.getAtoms()

    def getAtoms(self):
        atomList = []
        for i in range(self.natoms):
            atomInfo = {key: value[i] for key, value in self.nodes.items()}
            atomList.append(Atom(atomInfo))
        return atomList

    @property
    def natoms(self):
        return self.nnodes

    def getAtomByIdx(self, idx):
        fields = {key: value[idx] for key, value in self.nodes.items()}
        return Atom.fromAtom(fields)

    def setTopo(self, connection):
        self.topo.setTopo(connection)

    def getBonds(self) -> List[Bond]:
        bondIdx = self.topo.bonds
        if bondIdx is None:
            return []
        atoms = np.array(self.atoms)
        itoms = atoms[bondIdx[:, 0]]
        jtoms = atoms[bondIdx[:, 1]]
        bondTypes = self.topo._bondTypes
        bonds = []
        for i in range(len(bondIdx)):
            bonds.append(Bond(itoms[i], jtoms[i], bondTypes[i]))
        return bonds

    @property
    def nbonds(self) -> int:
        return self.topo.nbonds

    def getBondIdx(self) -> List[List]:
        return self.topo.bonds

    def getAngles(self) -> List[Angle]:
        angleIdx = self.topo.angles
        angleTypes = self.topo._angleTypes
        if angleIdx is None:
            return []
        atoms = np.array(self.atoms)
        itoms = atoms[angleIdx[:, 0]]
        jtoms = atoms[angleIdx[:, 1]]
        ktoms = atoms[angleIdx[:, 2]]
        
        angles = []
        for id, i in enumerate(1, range(len(angleIdx))):
            angles.append(Angle(id, itoms[i], jtoms[i], ktoms[i], angleTypes[i]))
        
        return angles

    @property
    def nangles(self) -> int:
        return self.topo.nangles

    def getAnglesIdx(self) -> List[List]:
        return self.topo.angles

    def getDihedrals(self) -> List[Dihedral]:

        dihedralIdx = self.topo.dihedrals
        dihedralTypes = self.topo._dihedralTypes
        if dihedralIdx is None:
            return []
        atoms = np.array(self.atoms)
        itoms = atoms[dihedralIdx[:, 0]]
        jtoms = atoms[dihedralIdx[:, 1]]
        ktoms = atoms[dihedralIdx[:, 2]]
        ltoms = atoms[dihedralIdx[:, 3]]
        dihedrals = []
        for id, i in enumerate(1, range(len(dihedralIdx))):
            dihedrals.append(Dihedral(id, itoms[i], jtoms[i], ktoms[i], ltoms[i], dihedralTypes[i]))

        return dihedrals

    @property
    def ndihedrals(self) -> int:
        return self.topo.ndihedrals

    def getDihedralIdx(self) -> List[List]:
        return self.topo.dihedrals        

class AtomVec:
    
    def __init__(self):
        
        self.atoms = Atoms()