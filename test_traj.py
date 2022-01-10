# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

import freud
import molpy as mp
from molpy.io.lmp import DataReader, DumpReader
from molpy.atoms import Atoms
from molpy.analysis import diffraction, density, cluster
from numpy.lib import recfunctions as rfn
import numpy as np

system_name = 'io_40_125_pe_10_20'
jname = f'tests/samples/mode1/{system_name}/{system_name}'

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

atoms.mergeFields(np.dtype([('id', 'i4'), ('mol', 'i4'), ('type', 'i4'), ('q', 'f8'), ('position', 'f8', 3)]))

box = dumpReader.frameMetaInfo.box[nframe]
box = list(map(float, box))
box = mp.Box(box[1]-box[0], box[3]-box[2], box[5]-box[4])
allPos = atoms.position
    
    # using traj
    # for molid in range(1, atoms.data['mol'].max()):
# molid = 1
# mol = atoms.data[atoms.data['mol'] == molid]
# molPos = mol['position']

type = 1
mol = atoms.data[np.logical_or(atoms.data['type'] == type, atoms.data['type'] == 2)]
molPos = mol['position']

# calc Sq
sqCalculator = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)

sqCalculator.compute((box, molPos))
        
# calc RDF

rdfCalculator = density.RDF(bins=100, r_max=5, r_min=0, normalize=True)
rdfCalculator.compute((box, allPos), reset=False)

# calc cluster

clusterCalculator = cluster.Cluster()
clusterCalculator.compute((box, allPos), neighbors=dict(r_max=1.5))
print(clusterCalculator.num_clusters)