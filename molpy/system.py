# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-12
# version: 0.0.1

from molpy.box import Box
from molpy.atoms import AtomVec
import numpy as np
from molpy.io import Readers

class System:
    
    def __init__(self, comment:str=''):
        
        self.comment = comment
        self._atomVec = AtomVec()
        self._box = None
        self._forcefield = None
        
        self._traj = None
        self._nFrames = None
        self._frame = None
        
    @property
    def atoms(self):
        return self._atomVec
        
    def set_box(self, Lx, Ly, Lz=0, xy=0, xz=0, yx=0, is2D=False):
        
        self._box = Box(Lx, Ly, Lz, xy, xz, yx, is2D)
    
    def load_data(self, dataFile:str, format:str, method='replace'):
        """load data from file

        Args:
            dataFile (str): path of data file
            format (str): format of data file
            method (str, optional): how to load the data. Defaults to 'replace'.
        """
        data_reader = Readers['DataReaders'][format](dataFile)

        if method == 'replace':
            atoms = data_reader.get_atoms()
            self._atomVec.replace_nodes(atoms._nodes)
        elif method == 'update':
            atoms = data_reader.get_atoms(issort=True)
            for key, value in atoms.node.items():
                self._atomVec.set_node(key, value)
        elif method == 'append':
            pass
        
    def load_traj(self, trajFile:str, format):
        
        self._traj = Readers['TrajReaders'][format](trajFile)
        self._nFrames = self._traj.nFrames
        return self._traj
    
    def select_frame(self, nFrame:int, method='replace'):
        
        frame = self._traj.get_frame(nFrame)
        atoms = self._traj.get_atoms()
        if method == 'replace':
            self._atomVec.replace_nodes(atoms._nodes)
        
        box = self._traj.get_box()
        self.set_box(box['Lx'], box['Ly'], box['Lz'], box.get('xy', 0), box.get('xz', 0), box.get('yx', 0), box.get('is2D', False))
        
    def sample(self, start, stop, interal, method='replace')->int:
        
        frame = np.arange(self._nFrames)[start:stop:interal]
        for f in frame:
            self.select_frame(f)
            yield f
        
    