# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-05
# version: 0.0.1

class Harmonic:

    def __init__(self, **kwargs):
        self.k = kwargs['k']
        self.r0 = kwargs['r0']

    def getEnergy(self, r):
        return 0.5 * self.k * (r - self.r0)**2

    def getForce(self, r):
        return self.k * (r - self.r0)
    
