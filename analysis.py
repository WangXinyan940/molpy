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

dataReader = DataReader(f'{jname}.data', atom_style='full')
dataReader.parse()
atomData = dataReader.atoms
bondData = dataReader.bonds
atoms = Atoms(len(atomData))
atoms.fromStructuredArray(atomData)
atoms._topo.constructConnectionFromBonds(bondData)

dumpReader = DumpReader(f'{jname}.dump')
dumpReader.pre_parse()

bonds = atoms._topo.getBonds()

nframes = dumpReader.nframes

nframe = 60

frame = dumpReader.parse(nframe)
atoms.fromStructuredArray(frame)


box = dumpReader.box
box = list(map(float, box))
box = mp.Box(box[1]-box[0], box[3]-box[2], box[5]-box[4])
allPos = atoms.position

# setup neighbor list 

# aq = freud.locality.AABBQuery(box=box, points=allPos)
# query_list = aq.query(allPos, dict(exclude_ii=True, r_max=5))
# nblist = query_list.toNeighborList()

# using traj
mols = []
for molid in range(1, atoms.data['mol'].max()):

    mol = atoms.data[atoms.data['mol'] == molid]
    mols.append(mol)

nmols = len(mols)

ios = atoms.data[atoms.data['mol'] < 126]
pes = atoms.data[np.logical_and(126 <= atoms.data['mol'],  atoms.data['mol']< 126+20)]
counterion = atoms.data[atoms.data['mol']> 146]


# calc RDF

freud_rdf = density.RDF(bins=50, r_max=10, r_min=0, normalize=True)
freud_rdf.compute((box, ios['position']), reset=False)
    # nomalize

# bins = freud_rdf.bin_centers
# rdf = freud_rdf.rdf#  / np.sum(len(ios))



# # calc Sq
# sqCalculator = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)

# sqCalculator.compute((box, counterion['position']))
        

# # calc cluster

# clusterCalculator = cluster.Cluster()
# clusterCalculator.compute((box, ios['position']), neighbors=dict(r_max=1.5))
