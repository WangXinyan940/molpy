
import espressomd
from espressomd.interactions import FeneBond
required_features = ['LENNARD_JONES']
espressomd.assert_features(required_features)
import espressomd.polymer
import numpy as np
from molpy.modeller.randomWalk import RandomWalkOnFcc


### setup system ###
system = espressomd.System(box_l=[10, 10, 10])
system.time_step = 0.01
system.cell_system.skin = 0.4
fene = FeneBond(k=30, d_r_max=1.5, r_0=1)
system.bonded_inter.add(fene)
lj_eps = 1.5
lj_sig = 1.0
lj_cut = 2.5 * lj_sig
system.non_bonded_inter[0, 0].lennard_jones.set_params(
    epsilon = lj_eps,
    sigma = lj_sig,
    cutoff = lj_cut,
    shift='auto'
)
system.force_cap = 20

### add polymers ###
rw = RandomWalkOnFcc(10, 10, 10)
rw.walkOnce(rw.findStart(), 10, )
positions = rw.getPositions()

polymers = espressomd.polymer.linear_polymer_positions(n_polymers=1, beads_per_chain=10, bond_length=1, seed=23)
for polymer in polymers:
    monomers = system.part.add(pos=polymer)
    previous_part = None
    for i, part in enumerate(monomers):
        if previous_part:
            part.add_bond((fene, previous_part))
            # part.add_exclusion(i-1)
        previous_part = part

### warmup ###
system.integrator.set_steepest_descent(f_max=0, gamma=1e-3, max_displacement=0.01)

max_iter = 10
i=0
while system.analysis.min_dist() < 0.9*lj_sig or i<max_iter:
    print(f"minimization: {system.analysis.energy()['total']:+.2e}")
    system.integrator.run(20)  
    i += 1  
    
print(f"minimization: {system.analysis.energy()['total']:+.2e}")
print()
system.integrator.set_vv()

# activate thermostat
system.thermostat.set_langevin(kT=1.0, gamma=1.0, seed=42)

print("simulating...")
t_steps = 1000
for t in range(t_steps):
    print(f"step {t + 1} of {t_steps}", end='\r', flush=True)
    system.integrator.run(10)
print('done')