# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-03
# version: 0.0.1

from molpy.atoms import Atoms

def toAtoms(positions, bonds):
    
    atoms = Atoms()
    atoms.setPositions(positions)   
    atoms.setTopo(bonds)
    
    return atoms
    