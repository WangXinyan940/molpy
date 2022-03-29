# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-28
# version: 0.0.1

import pint
from pint import UnitRegistry as unit
from pint import systems

def defReducedUnit(unitRegistry, base_length, base_mass, base_energy, kb=1):
    
    group_defination = [
         '@group Reduce',
        f'reduce_length = {base_length.magnitude} * {str(base_length.units)} = LJ_length',
        f'reduce_mass = {base_mass.magnitude} * {str(base_mass.units)} = LJ_mass',
        f'reduce_energy = {base_energy.magnitude} * {str(base_energy.units) }= LJ_energy',
         '@end'
    ]
    
    def _define_unit(definition):
        unitRegistry.define(definition)
    
    systems.Group.from_lines(group_defination, _define_unit)
    return unitRegistry
    

