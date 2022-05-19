# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.2


from molpy.atom import Atom
from molpy.atoms import AtomVec, Atoms
from molpy.forcefield import Forcefield
from molpy.io.lmp import DataReader, DumpReader
from molpy.neighborlist import NeighborList
from molpy.pair import Pair
from molpy.box import Box
from typing import List


class System:
    def __init__(self, comment=""):

        self.atomVec = AtomVec()
        self._box = None
        self._forcefield = Forcefield()
        self.comment = comment
    
    @property
    def boxVec(self):
        box = self._box
        return [box.Lx, box.Ly, box.Lz, box.xy, box.xz, box.yz]
    
    @property
    def forcefield(self):
        return self._forcefield

    @property
    def atoms(self):
        return self.atomVec.atoms
    
    @property
    def bonds(self):
        return self.atomVec.atoms.bonds
    
    @property
    def angles(self):
        return self.atomVec.atoms.angles
    
    @property
    def dihedrals(self):
        return self.atomVec.atoms.dihedrals

    @property
    def topo(self):
        return self.atomVec.atoms.topo

    @property
    def box(self):
        return self._box

    @property
    def forcefield(self):
        return self._forcefield

    @property
    def natoms(self):
        return self.atomVec.atoms.natoms

    @property
    def nbonds(self):
        return self.atomVec.atoms.nbonds

    @property
    def nangles(self):
        return self.atomVec.atoms.nangles

    @property
    def ndihedrals(self):
        return self.atomVec.atoms.ndihedrals
    
    @property
    def nimpropers(self):
        return self.atomVec.atoms.nimpropers
    
    @property
    def natomTypes(self):
        return self._forcefield.natomTypes
    
    @property
    def nbondTypes(self):
        return self._forcefield.nbondTypes
    
    @property
    def nangleTypes(self):
        return self._forcefield.nangleTypes
    
    @property
    def ndihedralTypes(self):
        return self._forcefield.ndihedralTypes
    
    @property
    def atomTypes(self):
        return self._forcefield.atomTypes
    
    @property
    def bondTypes(self):
        return self._forcefield.bondTypes

    def getAtoms(self)->List[Atom]:
        return self.atomVec.atoms.atoms

    def getBonds(self):
        return self.atomVec.atoms.getBonds()

    def getAngles(self):
        return self.atomVec.atoms.getAngles()

    def getDihedrals(self):
        return self.atomVec.atoms.getDihedrals()

    def getPairs(self, cutoff=None):
        if cutoff is None:
            cutoff = self._box / 2

        neighborList = NeighborList(self._box, self.atoms.positions)
        atoms = self.atoms
        pairs = [
            Pair(atoms[pair[0]], atoms[pair[1]], pair[2])
            for pair in neighborList.query(self.atoms.positions, dict(r_max=cutoff))
        ]
        return pairs
    
    def getForcefield(self):
        return self._forcefield()

    def loadData(self, dataFile, atom_style="full"):

        data_reader = DataReader(dataFile, atom_style=atom_style)
        atoms = data_reader.getAtoms()
        self.atomVec.atoms = atoms
        return atoms

    def loadAtoms(self, atomData, bondData):
        atoms = Atoms(fields=atomData)
        atoms.fromStructuredArray(atomData)
        atoms.setTopo(bondData)
        self.atomVec.atoms = atoms

    def loadTraj(self, dumpFile):

        self._traj = DumpReader(dumpFile)
        self.nFrames = self._traj.nFrames
        self.selectFrame(0)
        return self._traj

    def selectFrame(self, nFrame):

        frame = self._traj.getFrame(nFrame)
        atoms = frame['Atoms']
        
        for k in atoms.dtype.names:
            self.atomVec.atoms.nodes[k] = atoms[k]
        
        box = frame['box']
        self._box = Box(box[1] - box[0], box[3] - box[2], box[5] - box[4])

    def getAtomsStructuredArray(self):
        return self.atoms.toStructuredArray()

    def append(self, atoms):
        self.atomVec.append(atoms)

    def setBox(self, lx, ly, lz, xy=0, xz=0, yz=0):
        self._box = Box(lx, ly, lz, xy, xz, yz)

    def sample(self, start=0, stop=-1, interval=1):
        
        if stop == -1:
            stop = self.nFrames
        
        assert self._traj, AttributeError('Trajectory not loaded')
        assert stop <= self.nFrames, ValueError('Stop frame is less than the number of frames')
        assert start >= 0, ValueError('Start frame is larger than the number of frames')
        assert isinstance(interval, int), TypeError('Interval must be an integer')
        
        for nFrame in range(start, stop, interval):
            self.selectFrame(nFrame)
            yield self

    def save(self, path, format):
        
        pass
        