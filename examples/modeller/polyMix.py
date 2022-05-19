import molpy as mp
import numpy as np
from molpy.modeller import SimpleRW, toAtoms

""" Build a mix system with linear polyelectrolyte 
    and graft ionomer.
    ionomer:
        length of chain = 40
        number of chain = 5
        interval of charge group = 10
            o          o          o
        ----+----------+----------+
    polyelectrolyte:
        length of chain = 100
        number of chain = 10   
"""
box_size = 10
rw = SimpleRW(box_size)

# create linear polyelectrolyte
pe_lchain = 100
pe_nchain = 10
pe_bondLength = 1
pe_lists = []
for i in range(pe_nchain):
    
    positions = rw.walkOnce(pe_lchain, pe_bondLength)
    connects = rw.getLinearTopo(pe_lchain, offset=i*pe_lchain)
    atoms = toAtoms(positions, connects, f'pe{i}')
    pe_lists.append(atoms)
    
# create graft ionomer
io_lchain = 40
io_nchain = 5
interval = 10
io_bondLength = 1
io_lists = []
for i in range(io_nchain):
    
    main = rw.walkOnce(io_lchain, io_bondLength)
    graft_indices = np.arange(5, io_lchain, interval)
    graft_points = main[graft_indices]
    connects = rw.getLinearTopo(io_lchain, offset=i*io_lchain)
    for index, point in zip(graft_indices, graft_points):
        pos = rw.walkOnceFrom(point, 1, io_bondLength)
        main = np.vstack((main, point))
    graft_connects = rw.getGraftTopo(graft_indices, io_lchain)
    connects = np.vstack((connects, graft_connects))
    atoms = toAtoms(main, connects, f'io{i}')
    io_lists.append(atoms)
    
system = mp.System('io pe mixed system')
for io in io_lists:
    system.append(io)
for pe in pe_lists:
    system.append(pe)
    
dw = mp.DataWriter('./', )
dw.write(system, )

