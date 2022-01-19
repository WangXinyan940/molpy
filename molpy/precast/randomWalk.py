# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-12-11
# version: 0.0.1

from collections import deque
import numpy as np
from molpy.models.base import Model

sqrt2 = np.sqrt(2)
sqrt2_2 = sqrt2/2

rng = np.random.default_rng(10)

class RandomWalk(Model):
    def __init__(self,):

        pass

    def sarw(self, nchain, lchain, density, spacing, bc):

        nOccupiedSite = nchain * lchain

        total_site = int(nOccupiedSite / density)

        total_cell = total_site / 4  # FCC

        n_cell_per_side = int(np.cbrt(total_site)) + 1

        n_cell_x = n_cell_y = n_cell_z = n_cell_per_side

        lattice_size = np.array([n_cell_x, n_cell_y, n_cell_z])

        trial_step = np.zeros(4, dtype=int)
        current_step = np.zeros(4, dtype=int)
        next_step = np.zeros(4, dtype=int)

        rng = np.random.default_rng()
        sites = np.zeros((n_cell_x, n_cell_y, n_cell_z, 4), dtype=int)
        site_list = np.zeros((nOccupiedSite, 4), dtype=int)
        self.sites = sites
        self.site_list = site_list
        alternative_sites = np.zeros(
            (12, 4), dtype=int
        )  # 12 is coordinate number of FCC
        sqrt2_2 = np.sqrt(2) / 2

        bondIndices = np.zeros((nOccupiedSite, 2), dtype=int)
        nbond = np.array(0, dtype=int)

        def find_start(nstep):

            while True:
                start = rng.random(4)
                start[:3] *= lattice_size
                start[-1] *= 4
                start = start.astype(int)
                if sites[tuple(start)] == 0:
                    sites[tuple(start)] = 1
                    site_list[nstep] = start
                    nstep += 1
                    return start

        def map_site(l, mode="FCC"):
            if mode == "FCC":
                if l == 0:
                    a = np.array([0, 0, 0])
                elif l == 1:
                    a = np.array([0.5, 0.5, 0])
                elif l == 2:
                    a = np.array([0, 0.5, 0.5])
                else:
                    a = np.array([0.5, 0, 0.5])
                return a

        def apply_pbc(site):

            for i in range(3):
                if site[i] < 0:
                    site[i] = lattice_size[i] - 1
                if site[i] == lattice_size[i]:
                    site[i] = 0

        def isOccupied(site):

            if sites[tuple(site)] == 0:
                return False
            return True

        def _sarw(start, lchain, nstep):

            current_step = start
            n = 1
            v_queue = deque([], 3)
            norm_queue = deque([], 3)

            while n < lchain:

                nalter = 0
                angle = 0

                a = map_site(current_step[-1])
                angle = 0

                for dr in np.indices((3, 3, 3)).T.reshape(-1, 3) - 1:

                    trial_step[:3] = current_step[:3] + dr

                    for l in range(4):

                        trial_step[-1] = l
                        apply_pbc(trial_step)
                        if isOccupied(trial_step):
                            continue

                        aa = map_site(l)

                        v = aa + dr - a

                        distance = np.linalg.norm(v)

                        if distance < sqrt2_2 + 0.01:

                            if n != 1:

                                angle = (
                                    np.arccos(
                                        v_queue[-1] @ v / norm_queue[-1] / distance
                                    )
                                    * 180
                                    / np.pi
                                )

                            if (
                                (angle < -60 and angle > -150)
                                or (angle > 60 and angle < 150)
                                or n == 1
                            ):

                                alternative_sites[nalter] = trial_step
                                nalter += 1

                if nalter == 0:

                    sites[tuple(current_step)] = 2
                    current_step = site_list[nstep + n - 1]
                    n -= 1
                    nbond -= 1
                    nstep -= 1
                    v_queue.pop()
                    norm_queue.pop()

                else:

                    next_step = rng.choice(alternative_sites[:nalter])
                    sites[tuple(next_step)] = 1
                    site_list[n] = next_step
                    current_step = next_step
                    v_queue.append(v)
                    norm_queue.append(distance)
                    bondIndices[nbond] = (nstep - 1, nstep)
                    nbond += 1
                    n += 1
                    nstep += 1

        nstep = np.array(0)

        n = 0  # main chain
        while n < nchain:
            start = find_start(nstep)
            _sarw(start, lchain, nstep, nbond)
            n += 1

        # post-process
        # convert atom_list to coordinates in box
        positions = site_list[:, :3].astype(float)
        m = site_list[:, -1]
        positions[m == 1] += map_site(1)
        positions[m == 2] += map_site(2)
        positions[m == 3] += map_site(3)
        size_per_lattice = spacing / 0.707
        positions = positions * size_per_lattice

        return self.create_molecule("sarw", positions, bondIndices=bondIndices[:nbond])

class RandomWalkOnFCC(Model):
    
    def __init__(self, x, y, z, spacing, density=0.01, pbc=True) -> None:
        
        self.lattice_size = sqrt2 * spacing
        self.spacing = spacing
        nlattice_x = int(x/self.lattice_size)
        nlattice_y = int(y/self.lattice_size)
        nlattice_z = int(z/self.lattice_size)
        self.nlattice = np.array([nlattice_x, nlattice_y, nlattice_z], dtype=int)
        
        self.sites = np.zeros((nlattice_x, nlattice_y, nlattice_z, 4), dtype=int)
        
    def find_start(self):

        while True:
            start = rng.random(4)
            start[:3] *= self.nlattice
            start[-1] *= 4
            start = start.astype(int)
            if self.sites[tuple(start)] == 0:
                self.sites[tuple(start)] = 1
                return start
            
    def site2coord(self, l):
        if l == 0:
            a = np.array([0, 0, 0])
        elif l == 1:
            a = np.array([0.5, 0.5, 0])
        elif l == 2:
            a = np.array([0, 0.5, 0.5])
        else:
            a = np.array([0.5, 0, 0.5])
        return a
    
    def apply_bc(self, site, pbc=True):
        
        if pbc:
            for i in range(3):  # x, y, z
                if site[i] < 0:
                    site[i] = self.nlattice[i] - 1
                if site[i] == self.nlattice[i]:
                    site[i] = 0
            return site
        
    def isOccupied(self, site):
    
        if self.sites[tuple(site)] == 0:
            return False
        return True        
        
        
    def _rw(self, start, length, current_nstep, current_nbond):
        
        current_step = start
        nstep = current_nstep
        nbond = current_nbond
        n = 0
        b = 0
        v_queue = deque([], 3)
        norm_queue = deque([], 3)
        alternative_sites = np.zeros((12, 4), dtype=int)
        site_list = np.zeros((length, 4), dtype=int)
        bondIndices = np.zeros((length, 2), dtype=int)
        
        while n < length:
            
            nalter = 0
            angle = 0
            a = self.site2coord(current_step[-1])
            trial_step = np.zeros(4, dtype=int)
            
            for dr in np.indices((3, 3, 3)).T.reshape(-1, 3) - 1:

                trial_step[:3] = current_step[:3] + dr

                for l in range(4):

                    trial_step[-1] = l
                    self.apply_bc(trial_step)
                    if self.isOccupied(trial_step):
                        continue
                    
                    aa = self.site2coord(l)
                    v = aa + dr - a
                    distance = np.linalg.norm(v)
                    if distance < sqrt2_2 + 0.01 and distance > 0.01:
                        if n != 0:
                            angle =  np.arccos(
                                    v_queue[-1] @ v / norm_queue[-1] / distance
                                ) * 180 / np.pi
                                                      
                        if (
                            (angle < -60 and angle > -150)
                            or (angle > 60 and angle < 150)
                            or n == 0
                        ):
                            assert not np.array_equal(current_step, trial_step)
                            alternative_sites[nalter] = trial_step
                            nalter += 1
                                
            if nalter == 0:
                
                self.sites[tuple(current_step)] == 2
                n -= 1
                nbond -= 1
                current_step = site_list[n]
                v_queue.pop()
                norm_queue.pop()
                b-=1
                if len(v_queue) == 0 and len(norm_queue) == 0:
                    raise LookupError
                
            else:
                next_step = rng.choice(alternative_sites[:nalter])
                self.sites[tuple(next_step)] = 1
                site_list[n] = next_step
                current_step = next_step
                v_queue.append(v)
                norm_queue.append(distance)
                if n != 0:
                    bondIndices[b] = (nstep - 1, nstep)
                    b += 1
                    nbond += 1
                nstep += 1
                n += 1
            
        return site_list, bondIndices[:-1]
    
    def linear(self, length, out=None):
        
        nstep = 0
        nbond = 0
        tot_sites = np.zeros((length, 4), dtype=int)
        tot_bonds = np.zeros((length-1, 2), dtype=int)

        start = self.find_start()
        tot_sites[nstep] = start
        nstep += 1
        site_list, bondIndices = self._rw(start, length-1, nstep, nbond)
        tot_sites[nstep: nstep+length-1] = site_list
        tot_bonds[nbond] = (nstep-1, nstep)
        nstep += length-1
        nbond += 1
        tot_bonds[nbond: nbond+length-2] = bondIndices
        nbond += length - 1
        
        # post-process
        # convert atom_list to coordinates in box
        positions = tot_sites[:, :3].astype(float)
        m = tot_sites[:, -1]
        positions[m == 1] += self.site2coord(1)
        positions[m == 2] += self.site2coord(2)
        positions[m == 3] += self.site2coord(3)
        size_per_lattice = self.spacing / 0.707
        positions = positions * size_per_lattice
        
        if out is None:
            return positions, tot_bonds
        elif out.itemType == 'Molecule':
            names = [f'atom-{i}' for i in range(nstep)]
            out.create_atoms(names=names, positions=positions, bondIndices=tot_bonds)
            
    def graft(self, main_length, graft_points, graft_lengths, out=None):
        
        atomid = 0
        bondid = 0
        tot_sites = np.zeros((main_length+np.sum(graft_lengths), 4), dtype=int)
        tot_bonds = np.zeros((main_length-1+np.sum(graft_lengths), 2), dtype=int)

        start = self.find_start()
        tot_sites[atomid] = start
        atomid += 1
        site_list, bondIndices = self._rw(start, main_length-1, atomid, bondid)
        tot_sites[atomid: atomid+main_length-1] = site_list
        tot_bonds[bondid] = (atomid-1, atomid)  # link start and reminder
        bondid += 1
        tot_bonds[bondid: bondid+main_length-2] = bondIndices
        atomid += main_length-1
        bondid += main_length - 2


        for graft_point, graft_length in zip(graft_points, graft_lengths):
            start = tot_sites[graft_point]
            sites, bonds = self._rw(start, graft_length, atomid, bondid)
            tot_sites[atomid: atomid+graft_length] = sites
            tot_bonds[bondid] = (graft_point, atomid)
            tot_bonds[bondid+1: bondid+graft_length] = bonds
            atomid += graft_length
            bondid += graft_length
            
        # post-process
        # convert atom_list to coordinates in box
        positions = tot_sites[:, :3].astype(float)
        m = tot_sites[:, -1]
        positions[m == 1] += self.site2coord(1)
        positions[m == 2] += self.site2coord(2)
        positions[m == 3] += self.site2coord(3)
        positions = positions * self.lattice_size
                    
        if out is None:
            return positions, tot_bonds
        elif out.itemType == 'Molecule':
            names = [f'atom-{i}' for i in range(len(positions))]
            out.create_atoms(names=names, positions=positions, bondIndices=tot_bonds)
            
