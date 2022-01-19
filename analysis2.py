# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-16
# version: 0.0.1

import numpy as np
import molpy as mp
from molpy.analysis import diffraction, density, cluster
from tqdm import tqdm


            
def analysis(mode, lchain, ncharge, isSave):
    print('* * * * * *')
    system_name = f'io_40_125_pe_{lchain}_{int(ncharge/lchain)}'
    path = f'/home/roy/work/duan/paper/mode{mode}/{system_name}/'
    jname = f'{system_name}'

    system = mp.System()
    try:
        system.loadData(f'{path+jname}.data')
        system.loadTraj(f'{path+jname}.dump')
    except:
        print(f'mode{mode}, {jname} fails')
        
    
    nframes = system.nframes
    if nframes != 1001:
        print(f'mode{mode}, {jname} fails')
        

    # init kernel
    print(f'processing mode{mode}, {jname}')
    rdfKernel0 = density.RDF(bins=200, r_max=24, r_min=0)
    rdfKernel1 = density.RDF(bins=200, r_max=24, r_min=0)
    rdfKernel2 = density.RDF(bins=200, r_max=24, r_min=1, normalize=False)
    sqKernel = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)
    clusterKernel = cluster.Cluster()

    for nframe in tqdm(range(nframes)):
    # nframe = 99
        system.selectFrame(nframe)
        system._atoms.mergeFields(['x', 'y', 'z'], 'position')
        fields = system.getAtomsWithStructuredArray()
        box = system._box
        io = fields[np.logical_or(fields['type']==1 , fields['type']==3)]

        io_backbone = fields[fields['type']==1]
        # io_group = fields[fields['type']==3]
        # counterion = fields[fields['type']==4]

        
        
        io_pos = io['position']
        io_backbone_pos = io_backbone['position']
        # io_group_pos = io_group['position']
        # counterion_pos = counterion['position']


        # calc RDF
        # rdfKernel.compute((box, io_group_pos), query_points=counterion_pos, reset=False)

        # # cluster
        # allPos = fields['position']
        # poly = fields[fields['type']<4]
        # poly_pos = poly['position']
        pe = fields[fields['type']==3]
        pe_pos = pe['position']
        clusterKernel.compute((box, io_backbone_pos), neighbors=dict(r_max=1.5))
        
        cl_props = cluster.ClusterProperties()
        cl_props.compute((box, io_backbone_pos), clusterKernel.cluster_idx)
        COM = cl_props.centers
        rdfKernel1.compute((box, pe_pos), query_points=COM, reset=False)  # COM-pe
        rdfKernel2.compute((box, io_backbone_pos), query_points=COM, reset=False)  # COM-io

        # # calc sq
    # sqKernel.compute((box, io_pos), reset=True)
    
    
    
    if isSave:
        print(f'saving mode{i}, {jname}')
        np.savetxt(f'{path}rdf.csv', np.vstack((rdfKernel.bin_centers, rdfKernel.rdf)).T)
        np.savetxt(f'{path}sq.csv', np.vstack((sqKernel.bin_centers[1:], sqKernel.S_k[1:])).T)
        np.savetxt(f'{path}cluster.csv', np.array(list(map(len, clusterKernel.cluster_keys))))
            
nmode = 3
for i in range(nmode, nmode+1):
    for lchain in [10, 50, 100]:
        for ncharge in [200, 500, 800]:
            analysis(i, lchain, ncharge, isSave=True)