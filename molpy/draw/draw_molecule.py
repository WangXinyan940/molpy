# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-03
# version: 0.0.1

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def draw_molecule(positions, bonds, atom_settings={}, bond_settings={}):
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    for position in positions:
        ax.scatter(position[0], position[1], position[2], **atom_settings)
        
    for bond in bonds:
        pair = positions[bond]
        ax.plot(pair[0], pair[1])
        
    return ax

if __name__ == '__main__':
    
    positions = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1]])
    bonds = np.array([[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]])
    ax = draw_molecule(positions, bonds)
