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

pe_lchain = 00
pe_nchain = 00

system_name = f'io_40_125_pe_{pe_lchain}_{pe_nchain}'
jname = f'tests/paper/{system_name}/{system_name}'

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

# init calculator
rdfKernel = density.RDF(bins=200, r_max=24, r_min=0)
sqKernel = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)
clusterKernel = cluster.Cluster()

for nframe in [7, 8, 9]:

    frame = dumpReader.parse(nframe)
    atoms.fromStructuredArray(frame)


    box = dumpReader.box
    box = list(map(float, box))
    box = mp.Box(box[1]-box[0], box[3]-box[2], box[5]-box[4])
    atoms.mergeFields(['x', 'y', 'z'], 'position')
    fields = atoms.toStructuredArray()
    
    io = fields[np.logical_or(fields['type']==1 , fields['type']==3)]
    
    io_backbone = fields[fields['type']==1]
    io_group = fields[fields['type']==3]
    counterion = fields[fields['type']==4]

    io_pos = io['position']
    io_backbone_pos = io_backbone['position']
    io_group_pos = io_group['position']
    counterion_pos = counterion['position']


    # calc RDF
    rdfKernel.compute((box, io_group_pos), query_points=counterion_pos)
    
    # np.savetxt('rdf.csv', np.vstack((rdfKernel.bin_centers, rdfKernel.rdf)).T)
    
    # # calc sq
    sqKernel.compute((box, io_pos))
    # np.savetxt('sq.csv', np.vstack((sqKernel.bin_centers, sqKernel.S_k)).T)
    # # cluster
    clusterKernel.compute((box, io_pos), neighbors=dict(r_max=1.5))
    # np.savetxt('cluster.csv', np.array(list(map(len, clusterKernel.cluster_keys))))


# # calc Sq
# sqCalculator = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)

# sqCalculator.compute((box, counterion['position']))
        

# # calc cluster

# clusterCalculator = cluster.Cluster()
# clusterCalculator.compute((box, ios['position']), neighbors=dict(r_max=1.5))
