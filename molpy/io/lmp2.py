# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-12
# version: 0.0.1

__all__ = [
    'DataReader',
    'DataWriter',
    'DumpReader'
]

from typing import List
import numpy as np
from molpy.io.fileHandler import FileHandler

DUMP_TYPES = {
    
    'id': int,
    'mol': int,
    'type': int,
    'q': float,
    'x': float,
    'y': float,
    'z': float,

}


class DumpReader:
    
    def __init__(self, fpath:str):
        
        self.filepath = fpath
        self.filehandler = FileHandler(fpath)
        self.chunks = self.filehandler.readchunks('ITEM: TIMESTEP')
        
    def getframe(self, index):
        
        chunk = self.chunks.getchunk(index)
        
        return DumpReader.parse(chunk)
        
    @staticmethod
    def parse(chunk:List[str]):
        
        data = {}
        
        data['timestep'] = int(chunk[1])
        data['natoms'] = int(chunk[3])
        xlo, xhi = [float(x) for x in chunk[5].split()]
        ylo, yhi = [float(x) for x in chunk[6].split()]
        zlo, zhi = [float(x) for x in chunk[7].split()]
        data['box'] = [xlo, xhi, ylo, yhi, zlo, zhi]
        
        header = chunk[8].split()[2:]
        
        m = map(lambda x: tuple(x.split()), chunk[9:])
        lm = list(m)
        atomArr = np.array(lm, dtype={'names': header, 'formats': [DUMP_TYPES[k] for k in header]})
        
        data['atomInfo'] = atomArr
        
        return data
       
       
SECTIONS = [
    'Masses', 'Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers'
]

DATA_TYPES = {
    'atoms': int,
    'bonds': int,
    'angles': int,
    'dihedrals': int,
    'impropers': int,
    'atom types': int,
    'bond types': int,
    'angle types': int,
    'dihedral types': int,
    'improper types': int,
}
           
class DataReader:
    
    def __init__(self, fpath:str, atom_style:str='full'):
        
        self.filepath = fpath
        self.filehander = FileHandler(fpath)
        self.atom_style = atom_style
        
    def getdata(self):
        
        lines = self.filehander.readlines()
        data = DataReader.parse(lines, self.atom_style)
        return data
        
    @staticmethod
    def parse_line(line:str):
        
        return line.partition('#')[0].split()
        
    @staticmethod
    def parse(lines:List[str], atom_style:str='full'):
        
        data = {}
        
        data['comment'] = lines[0]
        
        for i, line in enumerate(lines[2:14]):
            
            line = DataReader.parse_line(line)
            
            for field, type in DATA_TYPES.items():
                
                if line[-1] == field:
                    data[field] = type(line[0])
                    break
                
            if line[-1] == 'xhi':
                break
                
        for line in lines[i+2:i+5]:
            
            line = DataReader.parse_line(line)
            
            if line[-1] == 'xhi':
                xlo = float(line[0])
                xhi = float(line[1])
                
            elif line[-1] == 'yhi':
                ylo = float(line[0])
                yhi = float(line[1])
                
            elif line[-1] == 'zhi':
                zlo = float(line[0])
                zhi = float(line[1])
        
        data['box'] = [xlo, xhi, ylo, yhi, zlo, zhi]
        
        section_start_lineno = {}
        
        for lino, line in enumerate(lines):
            
            line = DataReader.parse_line(line)
            if line and line[0] in SECTIONS:
                section_start_lineno[line[0]] = lino
           
                    
        #--- parse atoms ---
        atom_section_starts = section_start_lineno['Atoms'] + 2
        atom_section_ends = atom_section_starts + data['atoms']
        
        atomInfo = DataReader.parse_atoms(lines[atom_section_starts:atom_section_ends], atom_style=atom_style)
        data['Atoms'] = atomInfo
                    
        #--- parse bonds ---
        if 'Bonds' in section_start_lineno:
            bond_section_starts = section_start_lineno['Bonds'] + 2
            bond_section_ends = bond_section_starts + data['bonds'] + 1
            
            bondInfo = DataReader.parse_bonds(lines[bond_section_starts:bond_section_ends])
            data['Bonds'] = bondInfo
        
        # #--- parse angles ---
        if 'Angles' in section_start_lineno:
            angles_section_starts = section_start_lineno['Angles'] + 2
            angles_section_ends = angles_section_starts + data['angles'] + 1
            angleInfo = DataReader.parse_angles(lines[angles_section_starts:angles_section_ends])
            data['Angles'] = angleInfo
        
        # #--- parse dihedrals ---
        if 'Dihedrals' in section_start_lineno:
            dihedrals_section_starts = section_start_lineno['Dihedrals'] + 2
            dihedrals_section_ends = dihedrals_section_starts + data['dihedrals'] + 1
            dihedralInfo = DataReader.parse_dihedrals(lines[dihedrals_section_starts:dihedrals_section_ends])
            data['Dihedrals'] = dihedralInfo
        
        
        return data
        
    @staticmethod
    def parse_atoms(lines:List[str], atom_style='full'):
        
        atom_style_types = {
            'full': np.dtype([
                ('id', int),
                ('mol', int),
                ('type', int),
                ('q', float),
                ('x', float),
                ('y', float),
                ('z', float)
            ])
        }
        
        l = list(map(lambda x: tuple(x.split()), lines))
        
        atomInfo = np.array(l, dtype=atom_style_types[atom_style])
        
        return atomInfo
    
    @staticmethod
    def parse_bonds(lines:List[str]):
        
        return list(map(lambda x: list(map(int, x.split())), lines))
    
    @staticmethod
    def parse_angles(lines:List[str]):
        
        return list(map(lambda x: list(map(int, x.split())), lines))

    @staticmethod
    def parse_dihedrals(lines:List[str]):
        
        return list(map(lambda x: list(map(int, x.split())), lines))
    