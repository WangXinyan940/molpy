# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-12
# version: 0.0.2

import freud

class NeighborList:
    
    def __new__(cls, box, points, algorithm='AABBQuery'):
        if algorithm == 'AABBQuery':
            return freud.locality.AABBQuery(box, points)
        elif algorithm == 'LinkCell':
            return freud.locality.LinkCell(box, points)
        
    # def __init__(self, box, points, algorithm='AABBQuery'):
    #     pass
    