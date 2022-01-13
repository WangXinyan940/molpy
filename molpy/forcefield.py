# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-13
# version: 0.0.2

import os
import itertools
import xml.etree.ElementTree as etree
import math
import warnings
from math import sqrt, cos
from copy import deepcopy
from collections import defaultdict

_dataDirectories = None

def _getDataDirectories():
    global _dataDirectories
    if _dataDirectories is None:
        _dataDirectories = [os.path.join(os.path.dirname(__file__), 'data')]
        try:
            from pkg_resources import iter_entry_points
            for entry in iter_entry_points(group='openmm.forcefielddir'):
                _dataDirectories.append(entry.load()())
        except:
            pass # pkg_resources is not installed
    return 

def _convertParameterToNumber(param):
    return float(param)

class ForceField:
    
    def __init__(self, ):
        self._atomTypes = {}
        self._atomClasses = {}
        
    def loadXmlFile(self, *files):

        if isinstance(files, tuple):
            files = list(files)
        else:
            files = [files]

        trees = []

        i = 0
        while i < len(files):
            file = files[i]
            tree = None
            try:
                # this handles either filenames or open file-like objects
                tree = etree.parse(file)
            except IOError:
                for dataDir in _getDataDirectories():
                    f = os.path.join(dataDir, file)
                    if os.path.isfile(f):
                        tree = etree.parse(f)
                        break
            except Exception as e:
                # Fail with an error message about which file could not be read.
                # TODO: Also handle case where fallback to 'data' directory encounters problems,
                # but this is much less worrisome because we control those files.
                msg  = str(e) + '\n'
                if hasattr(file, 'name'):
                    filename = file.name
                else:
                    filename = str(file)
                msg += "ForceField.loadFile() encountered an error reading file '%s'\n" % filename
                raise Exception(msg)
            if tree is None:
                raise ValueError('Could not locate file "%s"' % file)
            
        # Load the atom types.
        
        """
            <AtomTypes>
                <Type name="380" class="OW" element="O" mass="15.999"/>
                <Type name="381" class="HW" element="H" mass="1.008"/>
            </AtomTypes>
        """

        for tree in trees:
            if tree.getroot().find('AtomTypes') is not None:
                for type in tree.getroot().find('AtomTypes').findall('Type'):
                    self.defAtomType(type.attrib)
                    
                """
            <BondTypes>
                <Type name1="380" name2="381" style="Harmonic" length="0.09572" k="376560"/>
            </BondTypes>
                """
                    
        for tree in trees:
            if tree.getroot().find('BondTypes') is not None:
                for type in tree.getroot().find('BondTypes').findall('Type'):
                    self.defBondType(type.attrib)
                    


    def defAtomType(self, parameters):
        """Define a new atom type."""
        name = parameters.get('name', KeyError)
        if name in self._atomTypes:
            raise ValueError('Found multiple definitions for atom type: '+name)
        atomClass = parameters.get('class', None)
        element = parameters.get('element', None)
        mass = parameters.get('mass', None)
        
        self._atomTypes[name] = AtomType(name, )
        
        if atomClass in self._atomClasses:
            typeSet = self._atomClasses[atomClass]
        else:
            typeSet = set()
            self._atomClasses[atomClass] = typeSet
        typeSet.add(name)
        self._atomClasses[''].add(name)
        
    def defBondType(self, parameters):
        
        if 'name1' in parameters and 'name2' in parameters:
            
            atom1 = self._atomTypes[parameters['name1']]
            atom2 = self._atomTypes[parameters['name2']]
        
        
class AtomType:
    
    def __init__(self, name):
        self.name = name