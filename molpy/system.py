# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.2


from molpy.atoms import AtomManager, Atoms
from molpy.forcefield import Forcefield
from molpy.io.lmp import DataReader, DumpReader
from molpy.neighborlist import NeighborList
from molpy.pair import Pair
from molpy.box import Box


class System:
    def __init__(self, comment=""):

        self._atomManager = AtomManager()
        # self._atoms = self._atomManager.atoms
        self._box = None
        self._forcefield = Forcefield()
        self.comment = comment

    @property
    def atomManager(self):
        return self._atomManager
    
    @property
    def forcefield(self):
        return self._forcefield

    @property
    def atoms(self):
        return self._atomManager.atoms
    
    @property
    def bonds(self):
        return self._atomManager.bonds
    
    @property
    def angles(self):
        return self._atomManager.angles
    
    @property
    def dihedrals(self):
        return self._atomManager.dihedrals

    @property
    def topo(self):
        return self.atoms.topo

    @property
    def box(self):
        return self._box

    @property
    def forcefield(self):
        return self._forcefield

    @property
    def natoms(self):
        return self.atoms.natoms

    @property
    def nbonds(self):
        return self.atoms.nbonds

    @property
    def nangles(self):
        return self.atoms.nangles

    @property
    def ndihedrals(self):
        return self.atoms.ndihedrals
    
    @property
    def nimpropers(self):
        return self.atoms.nimpropers
    
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

    def getAtoms(self):
        return self.atoms

    def getBonds(self):
        return self.atoms.getBonds()

    def getAngles(self):
        return self.atoms.getAngles()

    def getDihedrals(self):
        return self.atoms.getDihedrals()

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
        data_reader.parse()
        atomData = data_reader.atoms
        bondData = data_reader.bonds
        self.loadAtoms(atomData, bondData)

    def loadAtoms(self, atomData, bondData):
        atoms = Atoms(fields=atomData)
        atoms.fromStructuredArray(atomData)
        atoms.setTopo(bondData)
        self._atomManager.atoms = atoms

    def loadTraj(self, dumpFile):

        self._traj = DumpReader(dumpFile)
        # pre_parse()
        self.nframes = self._traj.nframes

    def selectFrame(self, nframe):

        frame = self._traj.parse(nframe)
        self.atoms.fromStructuredArray(frame)

        box = self._traj.box
        box = list(map(float, box))
        self._box = Box(box[1] - box[0], box[3] - box[2], box[5] - box[4])

    def getAtomsStructuredArray(self):
        return self.atoms.toStructuredArray()

    def append(self, atoms):
        self._atomManager.append(atoms)

    def setBox(self, lx, ly, lz, xy=0, xz=0, yz=0):
        self._box = Box(lx, ly, lz, xy, xz, yz)


