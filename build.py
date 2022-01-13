# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-12
# version: 0.0.1

import molpy as mp
import numpy as np

system = mp.System()
system.box = mp.Box.from_box([50, 50, 50])

#TODO: system.forcefield = ff = mp.ForceField()

io_lchain = 40
io_nchain = 125

for i in range(io_nchain):
    natoms = 40+4
    ionomer = mp.Molecule(natoms=natoms)
    ionomer.appendFields({
        'id': np.arange(natoms),
        'mol': i,
        'type': np.random.randint(1, 6, natoms),
        'position': np.random.random((natoms, 3))
    })
    system.addMolecule(ionomer)
