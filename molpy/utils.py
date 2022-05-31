# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-08
# version: 0.0.2

import numpy as np
from freud import cluster
from molpy.atoms import Atoms, Cluster
from typing import List

def fromDictToStruct(d:dict):
    names = d.keys()
    values = d.values()
    dtypes = [v.dtype for v in values]
    maxLength = max(map(len, values))
    arr = np.empty((maxLength, ), dtype=np.dtype(list(zip(names, dtypes))))
    for k, v in zip(names, values):
        arr[k] = v
        
    return arr

def fromStructToDict(arr:np.ndarray):
    return {k: arr[k] for k in arr.dtype.names}

def splitToCluster(box, atoms, settings:dict):
    
    if box is None:
        raise ValueError('box is required for cluster method')
    
    positions = atoms.getPositions()
    
    clusterKernel = cluster.Cluster()
    clusterProp = cluster.ClusterProperties()
    clusterKernel.compute((box, positions), **settings)
    clusterProp.compute((box, positions), clusterKernel.cluster_idx)
    
    keys = clusterProp.cluster_keys
    
    cluster_list = []
    for i,  key in enumerate(keys):
        
        subAtoms = atoms.getSubGraph(key)
        cluster = Cluster.fromCopy(subAtoms)
        cluster_list.append(cluster)
        
    return cluster_list
    
def split(keys:List[List], format=Atoms):
    
    atoms_list = []
    for key in keys:
        
        # nodes
        nodes = {field: value[key] for field, value in nodes.items()}
        
        # edges is not supported yet
        atoms_list.append(format.fromDict(nodes, None, None, None, f'atoms with keys {keys}'))
        
    return atoms_list