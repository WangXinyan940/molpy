# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-02
# version: 0.0.2

from typing import Iterable
import numpy as np
from collections import deque
from molpy.modeller.base import BaseModdler

class RandomWalk(BaseModdler):
    
    def __init__(self, seed=None) -> None:
        self.updateRng(seed)
        
    def updateRng(self, seed):
        self.rng = np.random.default_rng(seed)

class RandomWalkOnFcc(RandomWalk):
    
    def __init__(self, siteX, siteY, siteZ, stepLength=1) -> None:
        
        super().__init__()
        self._siteX = siteX
        self._siteY = siteY
        self._siteZ = siteZ
        self.stepLength = 1
        # self._site_size = np.array((siteX, siteY, siteZ, 4))
        self._sites = np.zeros((siteX, siteY, siteZ, 4), dtype=np.int8)
        
    def findStart(self):
        
        while True:
            start = self.rng.random(4)
            start *= np.array(self._sites.shape)
            start = start.astype(int)
            if self._sites[tuple(start)] == 0:
                self._sites[tuple(start)] == 1
                return start
            
    def wrap(self, site):
        
        for i in range(3):
            if site[i] < 0:
                site[i] = self._sites.shape[i] - 1
            elif site[i] == self._sites.shape[i]:
                site[i] = 0
        return site
    
    def sites2coord(self, site):
        m = site[:, -1]
        a = np.zeros((len(site), 3))
        a[m==0] = np.array([0., 0., 0.])
        a[m==1] = np.array([0.5, 0.5, 0.])
        a[m==2] = np.array([0., 0.5, 0.5])
        a[m==3] = np.array([0.5, 0., 0.5])
        return a + site[:, :3]
    
    def site2coord(self, site):
        m = site[-1]
        if m == 0:
            a = np.array([0, 0, 0])
        elif m == 1:
            a = np.array([0.5, 0.5, 0])
        elif m == 2:
            a = np.array([0, 0.5, 0.5])
        else:
            a = np.array([0.5, 0, 0.5])
        return a + site[:3]     
            
    def calcVector(self, siteA, siteB):
        
        return self.site2coord(self.wrap(siteA)) - self.site2coord(self.wrap(siteB))
    
    def isOccupied(self, site):
        
        return True if self._sites[tuple(site)] == 1 else False
            
    def walkOnce(self, start_site, nsteps, offset=0, exclude_start=False, start_idx=0):


        walk_path = np.zeros((nsteps, 4), dtype=int)
        bonds = []
        step_queue = deque([], 3)
        if exclude_start:
            nstep = 0
        else:
            walk_path[0] = start_site
            step_queue.append(start_site)
            nstep = 1
        next_site = None
        current_site = start_site

        v_queue = deque([], 2)
        n_queue = deque([], 2)

        # va = self.calcVector(previous_site, start_site)
        # na = np.linalg.norm(va) if va else 0
        # v_queue.append(va)
        # n_queue.append(na)        
        
        alter_site = np.zeros((12, 4), dtype=int)
        nalters = 0        
        angle = 0
        while nstep < nsteps:
            
            trial_site = np.zeros(4, dtype=int)
            current_coord = self.site2coord(current_site)
            # 
            for dr in np.indices((3, 3, 3)).T.reshape(-1, 3) - 1:
                
                trial_site[:3] = current_site[:3] + dr
                
                for m in range(4):
                    
                    trial_site[-1] = m
                    self.wrap(trial_site)
                    if self.isOccupied(trial_site):
                        continue
                    
                    trial_coord = self.site2coord(trial_site)
                    vb = trial_coord - current_coord
                    nb = np.linalg.norm(vb)
                    if nb < 0.708 and nb > 0.01:

                        if len(v_queue):  # not the first step
                            angle = np.arccos(v_queue[-1]@vb/n_queue[-1]/nb) * 180 / np.pi

                            if (angle < -60 and angle > -150) or (angle > 60 and angle < 150) or nstep == 1:
                                # assert not np.array_equal(current_site, trial_site)
                                alter_site[nalters] = trial_site
                                nalters +=1
                                
                        else:
                            alter_site[nalters] = trial_site
                            nalters +=1

            if nalters:
                
                next_site = self.rng.choice(alter_site[:nalters])
                self._sites[tuple(next_site)] = 1
                walk_path[nstep] = next_site
 
                if nstep:
                    bonds.append([nstep+offset-1, nstep+offset])
                
                vb = self.calcVector(current_site, next_site)
                v_queue.append(vb)
                
                nb = np.linalg.norm(vb)
                n_queue.append(nb)
                step_queue.append(next_site)
                # previous_site = current_site
                current_site = next_site
                nstep += 1
                nalters = 0
                
            else:
                raise ValueError
        
        positions = self.sites2coord(walk_path)
        if start_idx:
            bonds.insert(0, [start_idx, bonds[0][0]])
        
        return positions, bonds
    
    def linears(self, length_list, offset=0):
        
        pos_list = []
        bond_list = []
        
        for i, length in enumerate(length_list):

            start = self.findStart()
            _offset = 0 if i ==0 else length_list[i-1]
            _offset += offset
            positions, bonds = self.walkOnce(start, length, offset=_offset)
            pos_list.append(positions)
            bond_list.append(bonds)
            
        return pos_list, bond_list
    
    def linear(self, length, offset=0):
        start = self.findStart()
        positions, bonds = self.walkOnce(start, length, offset)
        return positions, bonds
    
    def graft(self, main_length, graft_length, graft_point, offset=0):
        
        pos_list = []
        bond_list = []
            
        start = self.findStart()
        positions, bonds = self.walkOnce(start, main_length, offset=offset)
        pos_list.append(positions)
        bond_list.append(bonds)
        offset += main_length
        
        for g, point in enumerate(graft_point):
            
            gLen = graft_length[g]
            start = positions[point]
            
            
            g_pos, g_bond = self.walkOnce(start, gLen, offset=offset, exclude_start=True, start_idx=point+offset)
            pos_list.append(g_pos)
            bond_list.append(g_bond)
            offset += gLen

        return np.concatenate(pos_list), np.concatenate(bond_list) 

