# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-05
# version: 0.0.2


from molpy.atoms import Atoms
from molpy.io.lmp import DataReader, DumpReader
from .box import Box

class System:
    
    def __init__(self):
        
        self._atoms = None
        self._box = None
        self._forcefield = None
        
    @property
    def atoms(self):
        return self._atoms
    
    @property
    def topo(self):
        return self._atoms.topo
    
    @property
    def box(self):
        return self._box
    
    @property
    def forcefield(self):
        return self._forcefield
        
    def getAtoms(self):
        return self._atoms
    
    def getBonds(self):
        return self._atoms.getBonds()
    
    def getAngles(self):
        return self._atoms.getAngles()
        
    def getDihedral(self):
        return self._atoms.getDihedral()

    def loadData(self, dataFile, atom_style='full'):
        
        data_reader = DataReader(dataFile, atom_style=atom_style)
        data_reader.parse()
        atomData = data_reader.atoms
        bondData = data_reader.bonds
        self.loadAtoms(atomData, bondData)
        
    def loadAtoms(self, atomData, bondData):
        atoms = Atoms(fields=atomData)
        atoms.fromStructuredArray(atomData)
        atoms.setTopo(bondData)
        self._atoms = atoms
        
    def loadTraj(self, dumpFile):
        
        self._traj = DumpReader(dumpFile)
        # pre_parse()
        self.nframes = self._traj.nframes
        
    def selectFrame(self, nframe):
        
        frame = self._traj.parse(nframe)
        self._atoms.fromStructuredArray(frame)
        
        box = self._traj.box
        box = list(map(float, box))
        self._box = Box(box[1]-box[0], box[3]-box[2], box[5]-box[4])
        
    def getAtomsStructuredArray(self):
        return self._atoms.toStructuredArray()
        