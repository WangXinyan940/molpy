import molpy as mp
from molpy.modeller import SimpleRW

""" Build a batch of ionomers with
    length of chain = 40
    number of chain = 5
    interval of charge group = 10
        o          o          o
    ----+----------+----------+
"""

lchain = 40
nchain = 5
interval = 10

rw = SimpleRW()
atoms_list = []
for i in range(nchain):
    
    rw.walkOnce(lchain)
    positions = rw.positions
    start_points = positions[5::10]
    for start in start_points:
        rw.walkOnceFrom(start, 1)
    
    links = rw.links
    
    atoms = mp.Atoms(f'ionomer{i}')
    atoms['positions'] = positions
    atoms.setTopo(links)
    atoms_list.append(atoms)
    rw.reset()


