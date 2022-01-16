import sys

sys.path.append("C:\\Users\\lijic\\work\\molpy")

import numpy as np
import molpy as mp
from molpy import toLAMMPS
from molpy.models.randomWalk import RandomWalkOnFCC
rng = np.random.default_rng()
rng.standard_normal(())

system = mp.System("IO with ni=10")
lx = 50
ly = 50
lz = 50
system.box = mp.Box(50, 50, 50)
system.box.periodic = True
# system.box.defByBoxLength(100, 100, 100)
system.forcefield = ff = mp.ForceField("LJ ff", unit="LJ")

# model linear pe
# Nb = 10
# io = mp.Group(f"ionomer=10")
# for i in range(Nb):
#     mon = mp.Atom(f'io{i}', position=(0.577*i, 0.577*i, 0.577*i))
#     io.addAtom(mon)
#     if i != 0:
#         io.addBondByIndex(i-1, i)

# neg = mp.Atom('anion', position=(0.577*4, 0.577*4, 0.577*6))

# io.addAtom(neg)
# io.addBondByIndex(-1, 5)


# Ni = 10
# ionomer = mp.Molecule('ionomer molecule')
# for i in range(Ni):
#     iocopy = io(name=f'ionomer{i}').move((0.577*10*i, 0.577*10*i, 0.577*10*i))
#     ionomer.addGroup(iocopy)
#     if i != 0:
#         ionomer.addBondByName(f'io9@ionomer{i-1}', f'io0@ionomer{i}')
io_lchain = 40
io_nchain = 125
rw = RandomWalkOnFCC(100, 100, 100, 0.8)
names = [f'io-{i}' for i in range(io_lchain)]
names.extend([f'anion-{i}' for i in range(4)])
for i in range(io_nchain):
    ionomer = mp.Molecule(f'ionomer{i}')
    rw.graft(io_lchain, [i*10+5 for i in range(4)], [1 for _ in range(4)], ionomer)
    # names.extend([f'cation-{i}' for i in range(i)])
    ionomer.setNames(names)

    # assert ionomer.natoms == io_lchain + 10, f'ionomer natoms is {ionomer.natoms}'
    # assert ionomer.nbonds == 99 + 10
    system.addMolecule(ionomer)

for i in range(int(125*40/10)):
    cation = mp.Atom(f'cation{i}', position=(0.577*5, 0.577*5, 0.577*7))
    vec = np.hstack(
    (
        rng.uniform(0, 50, 1),
        rng.uniform(0, 50, 1),
        rng.uniform(0, 50, 1),
    )
)
    system.addMolecule(cation.moveTo(vec))

pe_lchain = int(sys.argv[1])
pe_nchain = int(sys.argv[2])
names = [f'pe-{i}' for i in range(pe_lchain)]
for i in range(pe_nchain):
    pe = mp.Molecule(f'pe{i}')
    rw.linear(pe_lchain, pe)
    pe.setNames(names)
    system.addMolecule(pe)
    
for i in range(pe_nchain*pe_lchain):
    neg = mp.Atom(f'neg{i}', position=(0.577*5, 0.577*5, 0.577*7))
    vec = np.hstack(
    (
        rng.uniform(0, 50, 1),
        rng.uniform(0, 50, 1),
        rng.uniform(0, 50, 1),
    )
)
    system.addMolecule(neg.moveTo(vec))

# set up forcefield
T = 300  # room temperature
kb = 1.0  # bolzmann constant
sigma = 1.0  # =3.5A
eps0 = 1.0  # =kbT
m0 = 1.0
Z = 1.0 * 11.8

ff.defAtomType(  # backbone
    "io", mass=m0, charge=0, matchFunc=lambda atom: atom.name.startswith("io")
)
ff.defAtomType(  # pe chain
    "pe", mass=m0, charge=Z, matchFunc=lambda atom: atom.name.startswith("pe")
)
ff.defAtomType(  # io group
    "anion", mass=m0, charge=-Z, matchFunc=lambda atom: atom.name.startswith("anion")
)
ff.defAtomType(  # io counterion
    "cation", mass=m0, charge=Z, matchFunc=lambda atom: atom.name.startswith("cation")
)
# ff.defAtomType(  # 
#     "pos", mass=m0, charge=Z, matchFunc=lambda atom: atom.name.startswith("pos")
# )
ff.defAtomType(  # pe counterion
    "neg", mass=m0, charge=-Z, matchFunc=lambda atom: atom.name.startswith("neg")
)


ff.defBondType(
    "fene",
    style="fene",
    k=30 * eps0 / sigma ** 2,
    R0=1.5 * sigma,
    matchFunc=lambda bond: True,
)

ff.defNoneBondType("short-range", style="lj126", epsilon=2 * eps0, sigma=sigma)
ff.defNoneBondType("electrostatic", style="coul", C=kb * T * 2 * sigma)

# system.forcefield.render(ionomer, noAngle=True, noDihedral=True)


# build up

# ni = 170  # number of pe in system
# l=0
# for i in range(15):
#     for j in range(15):
#         if l < ni:
#             system.addMolecule(ionomer(name=f'io{i}-{j}').move((i*1.5, j*1.5, 0)))
#             l += 1

# assert system.natoms == 170 * 110, f'{system.natoms=}'

system.complete(noAngle=True, noDihedral=True)
# pos = mp.Atom('pos', position=(0.577*5, 0.577*5, 0.577*7))
# neg = mp.Atom('neg', position=(0.577*5, 0.577*5, 0.577*7))
# if pe_lchain*pe_nchain > (io_lchain * io_nchain)*0.1:
#     system.addSolvent(neg, ionicStrength=0)
# else:
#     system.addSolvent(pos, ionicStrength=0)

# assert system.natoms == 170 * 110 + 170*10
fname = f"io_{io_lchain}_{io_nchain}_pe_{pe_lchain}_{pe_nchain}.data"

toLAMMPS(fname, system, atom_style="full")
