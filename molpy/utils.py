
from molpy.atoms import Atoms

def data2atoms(data):
    
    atoms = Atoms(withTopo=True)
    for key, value in data['atoms'].items():
        atoms.set_atom_values(key, value)
        
    return atoms
    
    