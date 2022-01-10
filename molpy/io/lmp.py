# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-09
# version: 0.0.1
import numpy as np
from .base import ReaderBase


# Sections will all start with one of these words
# and run until the next section title
SECTIONS = set([
    'Atoms',  # Molecular topology sections
    'Velocities',
    'Masses',
    'Ellipsoids',
    'Lines',
    'Triangles',
    'Bodies',
    'Bonds',  # Forcefield sections
    'Angles',
    'Dihedrals',
    'Impropers',
    'Pair',
    'Pair LJCoeffs',
    'Bond Coeffs',
    'Angle Coeffs',
    'Dihedral Coeffs',
    'Improper Coeffs',
    'BondBond Coeffs',  # Class 2 FF sections
    'BondAngle Coeffs',
    'MiddleBondTorsion Coeffs',
    'EndBondTorsion Coeffs',
    'AngleTorsion Coeffs',
    'AngleAngleTorsion Coeffs',
    'BondBond13 Coeffs',
    'AngleAngle Coeffs',
])
# We usually check by splitting around whitespace, so check
# if any SECTION keywords will trip up on this
# and add them
for val in list(SECTIONS):
    if len(val.split()) > 1:
        SECTIONS.add(val.split()[0])


HEADERS = set([
    'atoms',
    'bonds',
    'angles',
    'dihedrals',
    'impropers',
    'atom types',
    'bond types',
    'angle types',
    'dihedral types',
    'improper types',
    'extra bond per atom',
    'extra angle per atom',
    'extra dihedral per atom',
    'extra improper per atom',
    'extra special per atom',
    'ellipsoids',
    'lines',
    'triangles',
    'bodies',
    'xlo xhi',
    'ylo yhi',
    'zlo zhi',
    'xy xz yz',
])


class LAMMPSIO:
    
    @staticmethod
    def _interpret_atom_style(atom_style=None, fields=None, formats=None):
        """interpret atom_style to fields

        Args:
            atom_style (str|list|tuple): LAMMPS' atom styles

        Returns:
            fields: fields in atom section
        """
        formats = {'id': int, 'mol': int, 'type': int, 'q': float, 'x': float, 'y': float, 'z': float}    
        atom_styles = {'full': ['id', 'mol', 'type', 'q', 'x', 'y', 'z'], 'molecular': ['id', 'mol', 'type', 'x', 'y', 'z']}
        if isinstance(atom_style, str):
            fields = atom_styles[atom_style]
            formats = [formats[field] for field in fields]
        
        elif fields:
            formats = [formats[field] for field in fields]
        
        else:
            raise ValueError    
        
        return fields, formats

class DataReader(ReaderBase, LAMMPSIO):
    
    format = ['data']

    def iterdata(self):
        with open(self.filename) as f:
            for line in f:
                line = line.partition('#')[0].strip()
                if line:
                    yield line

    def pre_parse(self):
        """Split a data file into dict of header and sections

        Returns:
            header: {property: value}
            sections: {section: dataliens}
        """
        
        f = list(self.iterdata())

        # line number of section start
        section_startline_no = [i for i, line in enumerate(f)
                  if line.split()[0] in SECTIONS]
        section_startline_no += [None]
        
        header = {}
        for line in f[:section_startline_no[0]]:
            for token in HEADERS:
                if line.endswith(token):
                    header[token] = line.split(token)[0]
                    continue

        sections = {f[l]:f[l+1:section_startline_no[i+1]]
                 for i, l in enumerate(section_startline_no[:-1])}
        
        return header, sections
 
    def parse(self, atom_style, fields=None, formats=None):
        """Parses a LAMMPS_ DATA file.
        """
        # Can pass atom_style to help parsing
        fields, formats = self._interpret_atom_style(atom_style)

        header, sections = self.pre_parse()
        
        if 'Masses' in sections:
            self.masses = self._parse_masses(sections['Masses'])
        
        if 'Atoms' in sections:
            self.atoms = self._parse_atoms(sections['Atoms'], fields, formats)
        else:
            raise KeyError("Data file was missing Atoms section")
        
        if 'Bonds' in sections:
            self.bonds = self._parse_bonds(sections['Bonds'])
            

    def _parse_vel(self, datalines, order):
        """Strip velocity info into np array
        Parameters
        ----------
        datalines : list
          list of strings from file
        order : np.array
          array which rearranges the velocities into correct order
          (from argsort on atom ids)
        Returns
        -------
        velocities : np.ndarray
        """
        vel = np.zeros((len(datalines), 3), dtype=np.float32)

        for i, line in enumerate(datalines):
            line = line.split()
            vel[i] = line[1:4]

        vel = vel[order]

        return vel

    def _parse_bonds(self, datalines):

        m = map(lambda x: x.split(), datalines)
        bondArr = np.array(list(m), int)
        return bondArr[:, [2, 3, 1]]  # [atom1, atom2, bondtype]

    def _parse_atoms(self, datalines, fields, formats, massdict=None):

        m = map(lambda x: tuple(x.split()), datalines)
        atomArr = np.array(list(m), dtype={'names':fields, 'formats':formats})
            
        return atomArr

    def _parse_masses(self, datalines):
        """Lammps defines mass on a per atom type basis.
        This reads mass for each type and stores in dict
        """
        
        masses = {}
        for line in datalines:
            line = line.split()
            masses[line[0]] = float(line[1])

        return masses

    def _parse_box(self, header):
        x1, x2 = np.float32(header['xlo xhi'].split())
        x = x2 - x1
        y1, y2 = np.float32(header['ylo yhi'].split())
        y = y2 - y1
        z1, z2 = np.float32(header['zlo zhi'].split())
        z = z2 - z1

        if 'xy xz yz' in header:
            # Triclinic
            unitcell = np.zeros((3, 3), dtype=np.float32)
            xy, xz, yz = np.float32(header['xy xz yz'].split())
            unitcell[0][0] = x
            unitcell[1][0] = xy
            unitcell[1][1] = y
            unitcell[2][0] = xz
            unitcell[2][1] = yz
            unitcell[2][2] = z
            return unitcell
        else:
            # Orthogonal
            unitcell = np.zeros(6, dtype=np.float32)
            unitcell[:3] = x, y, z
            unitcell[3:] = 90., 90., 90.

            return unitcell
        
class FrameMetaInfo:
    
    def __init__(self):
        self.start_lino = []
        self.start_byte = []
        self.timesteps = []
        self.natoms = []
        self.box = []
        self.header = []
    
    @property
    def nFrames(self):
        return len(self.timesteps)
        
class DumpReader(ReaderBase, LAMMPSIO):
    
    format = ['dump']
    
    def pre_parse(self):
        isHeader = True
        frameMetaInfo = FrameMetaInfo()
        with open(self.filename) as f:

            line = f.readline()
            lino = 1
            while line:
                if line.startswith('ITEM: TIMESTEP'):
                    frameMetaInfo.start_lino.append(lino)
                    frameMetaInfo.start_byte.append(f.tell()-len(line))
                    line = f.readline()
                    frameMetaInfo.timesteps.append(int(line))
                    line = f.readline()  # ITEM: NUMBER OF ATOMS
                    frameMetaInfo.natoms.append(int(f.readline()))
                    line = f.readline()  # ITEM: BOX
                    frameMetaInfo.box.append((f.readline().split()+f.readline().split()+f.readline().split()))
                    line = f.readline()
                    if isHeader:
                        isHeader = False
                        frameMetaInfo.header = line.split()[2:]
                    lino += 8
                    
                line = f.readline()
                lino += 1
            frameMetaInfo.start_byte.append(f.tell())
        self.frameMetaInfo = frameMetaInfo
        
    def parse(self, frame=1):
        
        if not isinstance(frame, int):
            raise TypeError
        
        start_byte = self.frameMetaInfo.start_byte[frame]
        end_btyte = self.frameMetaInfo.start_byte[frame+1]
        size = end_btyte - start_byte
        header = self.frameMetaInfo.header
        fields, formats = LAMMPSIO._interpret_atom_style(fields=header)
        with open(self.filename) as f:
            f.seek(start_byte)
            datalines = f.read(size-1)
            datalines = datalines.split('\n')
            
            atomArr = self._parse_atoms(datalines[9:], fields, formats)
        return atomArr
            
    def _parse_atoms(self, datalines, fields, formats):
        
        m = map(lambda x: tuple(x.split()), datalines)
        lm = list(m)
        atomArr = np.array(lm, dtype={'names':fields, 'formats':formats})     
        return atomArr
    
    def getFrames(self, frames):
        for i in frames:
            yield self.parse(i)
 
    