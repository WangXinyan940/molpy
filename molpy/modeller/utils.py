# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-05-19
# version: 0.0.1

from ..atoms import Atoms

def toAtoms(positions, topo, name=None):
    
    atoms = Atoms(name)
    atoms.setTopo(topo)
    atoms['positions'] = positions
    
    return atoms