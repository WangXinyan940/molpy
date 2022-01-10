# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

import freud
import molpy as mp
from molpy.io.lmp import DataReader, DumpReader
from molpy.atoms import Atoms
from molpy.analysis import diffraction
import numpy as np

jname = 'tests/samples/io_50_100_pe_50_50'
system_name = 'test'

dataReader = DataReader(f'{jname}.data')
dataReader.parse('full')
dumpReader = DumpReader(f'{jname}.dump')
dumpReader.pre_parse()
atomData = dataReader.atoms
bondData = dataReader.bonds
atoms = Atoms(len(atomData), atomData.dtype)
atoms._topo.fromBondList(bondData[:, :2], bondData[:, -1])

bonds = atoms._topo.getBonds()

nFrames = dumpReader.frameMetaInfo.nFrames

# for nframe in range(0, nFrames, 3):
nframe = 3
    # load traj
frame = dumpReader.parse(nframe)
for field in frame.dtype.names:
    if field in atoms.data.dtype.names:
        atoms.data[field] = frame[field]
    
box = dumpReader.frameMetaInfo.box[nframe]
box = list(map(float, box))
box = freud.Box(box[1]-box[0], box[3]-box[2], box[5]-box[4])
    
    # using traj
    # for molid in range(1, atoms.data['mol'].max()):
molid = 1
mol = atoms.data[atoms.data['mol'] == molid]
position = np.hstack([mol['x'].reshape((len(mol), 1)), mol['y'].reshape((len(mol), 1)), mol['z'].reshape((len(mol), 1))])

# calc Sq
sqCalculator = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)

sqCalculator.compute((box, position))
        