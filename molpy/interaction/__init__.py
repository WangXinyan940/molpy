# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-05
# version: 0.0.1

from molpy.interaction.bond import *

class Register:
    
    def __init__(self):
        self._bond = {}
        self._angle = {}
        
    def getBondInteraction(self, name):
        return self._bond[name]
    
    def registerBondInteraction(self, name, bond):
        self._bond[name] = bond

register = Register()
register.registerBondInteraction('harmonic', Harmonic)
register.registerBondInteraction('Harmonic', Harmonic)
register.registerBondInteraction('HarmonicBondForce', Harmonic)