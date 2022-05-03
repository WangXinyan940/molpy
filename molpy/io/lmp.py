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
from molpy.atoms import Atoms
from molpy.io.fileHandler import FileHandler
from molpy.utils import fromStructToDict

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
        
    def getFrame(self, index):
        
        chunk = self.chunks.getchunk(index)
        
        return DumpReader.parse(chunk)
    
    @property
    def nFrames(self):
        return self.chunks.nchunks
        
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
        atomArr = np.array(lm, dtype={'names': header, 'formats': [DUMP_TYPES.get(k, float) for k in header]})
        
        data['Atoms'] = atomArr
        
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
        
    def getData(self):
        data = {}
        lines = self.filehander.readlines()
        data['comment'] = lines[0]
        lines = map(lambda line: DataReader.parse_line(line), lines)
        lines = list(filter(lambda line: line != (), lines))
        data.update(DataReader.parse(lines, self.atom_style))
        return data
    
    def getAtoms(self):
        
        data = self.getData()
        nodes = fromStructToDict(data['Atoms'])
        edges = {'bondType': data['Bonds']['type']}
        topo = [[i, j] for i, j in zip(data['Bonds']['itom'], data['Bonds']['jtom'])]
        atoms = Atoms.fromDict(nodes, edges, {}, topo)
        assert data['atoms'] == nodes['id'].__len__()
        return atoms
        
        
    @staticmethod
    def parse_line(line:str):
        
        return tuple(line.partition('#')[0].split())
        
    @staticmethod
    def parse(lines:List[str], atom_style:str='full'):
        
        data = {}

        for i, line in enumerate(lines):
            
            for field, type in DATA_TYPES.items():
                
                if line[-1] == field:
                    data[field] = type(line[0])
                    break
            
            if line[-1] == 'xhi':
                break
                
                
        for line in lines[i:i+3]:
            
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

            if line and line[0] in SECTIONS:
                section_start_lineno[line[0]] = lino
           
                    
        #--- parse atoms ---
        atom_section_starts = section_start_lineno['Atoms'] + 1
        atom_section_ends = atom_section_starts + data['atoms']
        
        atomInfo = DataReader.parse_atoms(lines[atom_section_starts:atom_section_ends], atom_style=atom_style)
        data['Atoms'] = atomInfo
                    
        #--- parse bonds ---
        if 'Bonds' in section_start_lineno:
            bond_section_starts = section_start_lineno['Bonds'] + 1
            bond_section_ends = bond_section_starts + data['bonds'] + 1
            
            bondInfo = DataReader.parse_bonds(lines[bond_section_starts:bond_section_ends])
            data['Bonds'] = bondInfo
        
        # #--- parse angles ---
        if 'Angles' in section_start_lineno:
            angles_section_starts = section_start_lineno['Angles'] + 1
            angles_section_ends = angles_section_starts + data['angles'] + 1
            angleInfo = DataReader.parse_angles(lines[angles_section_starts:angles_section_ends])
            data['Angles'] = angleInfo
        
        # #--- parse dihedrals ---
        if 'Dihedrals' in section_start_lineno:
            dihedrals_section_starts = section_start_lineno['Dihedrals'] + 1
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
        # lines = list(map(lambda line: tuple(line), lines))
        atomInfo = np.array(lines, dtype=atom_style_types[atom_style])
        
        return atomInfo
    
    @staticmethod
    def parse_bonds(lines:List[str]):

        return np.array(lines, dtype=[('id', int), ('type', int), ('itom', int), ('jtom', int)])
    
    @staticmethod
    def parse_angles(lines:List[str]):
        
        return np.array(lines, dtype=[('id', int), ('type', int), ('itom', int), ('jtom', int), ('ktom', int)])

    @staticmethod
    def parse_dihedrals(lines:List[str]):
        
        return np.array(lines, dtype=[('id', int), ('type', int), ('itom', int), ('jtom', int), ('ktom', int), ('ltom', int)])
    
class DataWriter:
    
    def __init__(self, fpath:str, atom_style='full'):
        
        self.filepath = fpath
        self.filehander = FileHandler(fpath, 'w')
        self.atom_style = atom_style
        
    def write(self, system, isBonds=True, isAngles=True, isDihedrals=True):
        
        write = self.filehander.writeline
        
        #--- write comment ---
        write('# '+system.comment)
        write('\n\n')
        
        #--- write profile ---
        write(f'    {system.natoms} atoms\n')
        write(f'    {system.nbonds} bonds\n')
        # write(f'    {system.nangles} angles\n')
        # write(f'    {system.ndihedrals} dihedrals\n')
        # write(f'    {system.nimpropers} impropers\n')
        write(f'    {system.natomTypes} atom types\n')
        write(f'    {system.nbondTypes} bond types\n')
        # write(f'    {system.nangleTypes} angle types\n')
        # write(f'    {system.ndihedralTypes} dihedral types\n')
        # write(f'    {system.nimproperTypes} improper types\n')
        write('\n')
        
        #--- write box ---
        write(f'    {system.box.xlo} {system.box.xhi} xlo xhi\n')
        write(f'    {system.box.ylo} {system.box.yhi} ylo yhi\n')
        write(f'    {system.box.zlo} {system.box.zhi} zlo zhi\n')
        write('\n')
        
        #--- write masses section ---
        write('Masses\n\n')
        id = np.arange(system.natomTypes) + 1
        for i, at in enumerate(system.atomTypes):
            write(f'    {id[i]}    {at.mass}  # {at.name}\n')
        write('\n')
        
        #--- write atoms section ---
        write('Atoms\n\n')
        if 'id' not in system.atomManager.atoms:
            id = np.arange(system.natoms) + 1
        else:
            id = system.atomManager.atoms._fields['id']
        
        type_map = {}
            
        for i, at in enumerate(system.atoms):
            if not isinstance(at.type, int):
                type = type_map.get(at.type, len(type_map)) + 1
            write(f'    {id[i]}    {at.mol}    {type}    {at.q}    {at.x:.4f}    {at.y:.4f}    {at.z:.4f}\n')
        write('\n')
        
        #--- write bonds section ---
        if isBonds:
            id = np.arange(system.nbonds) + 1
            write('Bonds\n\n')
            for i, b in enumerate(system.bonds):
                write(f'    {id[i]}    {b.type}    {b[0].id}    {b[1].id}\n')
            write('\n')
        
        #--- write angle section ---
        if isAngles:
            write('Angles\n\n')
            for a in system.angles:
                write(f'    {a.id}    {a.type}    {a[0]}    {a[1]}    {a[2]}\n')
            write('\n')
            
        #--- write dihedral section ---
        if isDihedrals:
            write('Dihedrals\n\n')
            for d in system.dihedrals:
                write(f'    {a.id}    {d.type}    {d[0]}    {d[1]}    {d[2]}    {d[3]}\n')
            write('\n')
        
        self.filehander.close()    
    