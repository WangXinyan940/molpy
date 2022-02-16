# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-16
# version: 0.0.1

import numpy as np
from collections import Counter
import molpy as mp
# from molpy.analysis import diffraction, density, cluster
from freud import diffraction, density, cluster
from tqdm import tqdm
from glob import glob
import os

def checkIsComplete(path, nmode=None):

    not_complete = []

    if nmode is None:
        path = path + 'mode*/'
        modePaths = glob(path)
        if len(modePaths) == 0:
            raise ValueError
        for modePath in modePaths:
            dataPaths = glob(modePath+'io*')
            if len(dataPaths) == 0:
                raise ValueError
            for dataPath in dataPaths:
                os.chdir(dataPath)
                if len(glob('*3e6.data')) == 0:
                    not_complete.append(dataPath.split('/')[-2:])
    else:
        modePath = path + nmode +'/'
        dataPaths = glob(modePath+'io*')
        for dataPath in dataPaths:
            os.chdir(dataPath)
            if len(glob('*3e6.data')) == 0:
                not_complete.append(dataPath.split('/')[-2:])
    
    return not_complete

def analysis(dataDir, isSave=False):
    print(f'processing mode {dataDir}')
    os.chdir(dataDir)
    if glob(dataDir+'*3e6.data'):
        raise ValueError('not complete')
    dataName = dataDir.split('/')[-1]
    system = mp.System()
    try:
        print(f'load data')
        system.loadData(f'{dataName}.data')
        print(f'load dump')
        system.loadTraj(f'{dataName}.eq.dump')
    except:
        raise ValueError(f'not found')
        
    
    nframes = system.nframes
    if nframes != 2001:
        raise ValueError(f'not complete')
        

    # init kernel

    # calc group-ion
    rdfKernel0 = density.RDF(bins=200, r_max=24, r_min=0)
    # calc 
    rdfKernel1 = density.RDF(bins=200, r_max=24, r_min=0)
    # calc
    rdfKernel2 = density.RDF(bins=200, r_max=24, r_min=0)

    sqKernel = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)
    clusterKernel = cluster.Cluster()

    for nframe in tqdm(range(1000, nframes)):
        system.selectFrame(nframe)
        system._atoms.mergeFields(['x', 'y', 'z'], 'position')
        fields = system.getAtomsStructuredArray()
        box = system._box

        # packing
        allPos = fields['position']
        poly = fields[fields['type']<4]
        poly_pos = poly['position']
        
        io = fields[np.logical_or(fields['type']==1 , fields['type']==3)]
        io_backbone = fields[fields['type']==1]
        io_group = fields[fields['type']==3]
        io_counterion = fields[fields['type']==4]

        io_pos = io['position']
        io_backbone_pos = io_backbone['position']
        io_group_pos = io_group['position']
        io_counterion_pos = io_counterion['position']

        pe = fields[fields['type']==2]
        pe_pos = pe['position']

        # calc RDF
        rdfKernel0.compute((box, io_group_pos), query_points=io_counterion_pos, reset=False)

        # # cluster
        clusterKernel.compute((box, io_backbone_pos), neighbors=dict(r_max=1.5))
        
        cl_props = cluster.ClusterProperties()
        cl_props.compute((box, io_backbone_pos), clusterKernel.cluster_idx)
        COM = cl_props.centers

        rdfKernel1.compute((box, COM), query_points=io_backbone_pos, reset=False)  # COM-io

        rdfKernel2.compute((box, COM), query_points=pe_pos, reset=False)  # COM-pe

        
        # # calc sq
    sqKernel.compute((box, io_pos), reset=True)
    
    gyration_tensor = cl_props.gyrations
    Rg = cl_props.radii_of_gyration
    asphericity = cl_props.asphericity
    prolateness = cl_props.prolateness
    
    if isSave:
        print(f'saving')
        np.savetxt(f'{dataDir}/rdf0.csv', np.vstack((rdfKernel0.bin_centers, rdfKernel0.rdf)).T)
        np.savetxt(f'{dataDir}/rdf1.csv', np.vstack((rdfKernel1.bin_centers, rdfKernel1.rdf)).T)
        np.savetxt(f'{dataDir}/rdf2.csv', np.vstack((rdfKernel2.bin_centers, rdfKernel2.rdf)).T)
        np.savetxt(f'{dataDir}/sq.csv', np.vstack((sqKernel.bin_centers[1:], sqKernel.S_k[1:])).T)
        np.savetxt(f'{dataDir}/cluster.csv', np.array(list(map(len, clusterKernel.cluster_keys))))
        np.savetxt(f'{dataDir}/gyration.csv', gyration_tensor.reshape((-1, 9)))
        np.savetxt(f'{dataDir}/shape.csv', np.array([Rg, asphericity, prolateness]).T, fmt='%.4f')
            

if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':

        path = f'/home/lijichen/work/duan/paper/'
        nmode = 'mode1/'
        dataDir = glob(path+nmode+'io*')[5]
        # for data in dataDir[-1:]:
        #     analysis(data, isSave=True)
        os.chdir(dataDir)
        if glob(dataDir+'*2e6.data'):
            raise ValueError('not complete')
        dataName = dataDir.split('/')[-1]
        system = mp.System()
        try:
            system.loadData(f'{dataName}.data')
            system.loadTraj(f'{dataName}.dump')
        except:
            raise ValueError(f'not found')
            
        
        nframes = system.nframes
        if nframes != 1001:
            raise ValueError(f'not complete')
            

        # init kernel
        print(f'processing {dataDir}')

        sqKernel = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)
        clusterKernel = cluster.Cluster()
        
        os.chdir(dataDir)
        if glob(dataDir+'*2e6.data'):
            raise ValueError('not complete')
        dataName = dataDir.split('/')[-1]
        system = mp.System()
        try:
            system.loadData(f'{dataName}.data')
            system.loadTraj(f'{dataName}.dump')
        except:
            raise ValueError(f'not found')

        nframe = 1
        system.selectFrame(nframe)
        system._atoms.mergeFields(['x', 'y', 'z'], 'position')
        fields = system.getAtomsStructuredArray()
        box = system._box

        # packing
        allPos = fields['position']
        poly = fields[fields['type']<4]
        poly_pos = poly['position']
        
        io = fields[np.logical_or(fields['type']==1 , fields['type']==3)]
        io_backbone = fields[fields['type']==1]
        io_group = fields[fields['type']==3]
        io_counterion = fields[fields['type']==4]

        io_pos = io['position']
        io_backbone_pos = io_backbone['position']
        
        molid = poly['mol']

        # # cluster
        clusterKernel.compute((box, poly_pos), neighbors=dict(r_max=1.5))
        cluster_atteched_pe = np.where(poly['type']==2, clusterKernel.cluster_idx, -1)
        cluster_atteched_pe = Counter(cluster_atteched_pe)
        
        print(cluster_atteched_pe)
        
        rate_atteched_cluster = len(cluster_atteched_pe)/clusterKernel.num_clusters
        
        print(f'total: {rate_atteched_cluster}')
        
        
        cl_props = cluster.ClusterProperties()
        cl_props.compute((box, poly_pos), clusterKernel.cluster_idx)
        COM = cl_props.centers

        rdfKernel0 = density.RDF(bins=200, r_max=24, r_min=0)
        rdfKernel0.compute((box, COM), query_points=io_backbone_pos, reset=False)
        
        print(rdfKernel0.rdf)
        
        gyration_tensor = cl_props.gyrations
        
        

    else:
        path = f'/home/lijichen/work/duan/paper/'
        nmode = 'mode1/'
        dataDir = glob(path+nmode+'io*')
        print(len(dataDir))
        for data in dataDir:
            analysis(data, isSave=True)
