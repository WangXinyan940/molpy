# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

from collections import defaultdict
from itertools import combinations
import jax.numpy as jnp

from .angle import Angles
from .bond import Bonds
from .dihedral import Dihedrals


class Topo:
    
    def __init__(self, atoms=None, connection=None):
        
        self.reset()
        self.loadTopo(connection)
        
        if atoms is not None: 
            self.setAtoms(atoms)

    @property
    def adjDict(self):
        return self._adjDict

    @property
    def adjList(self):
        return self._adjList

    @property
    def adjMatrix(self):
        pass

    def reset(self):
        self._atoms = None
        self._bonds = None
        self._angles = None
        self._dihedrals = None
        self._hasBond = False
        self._hasAngle = False
        self._hasDihedral = False    
        self._hasAtom = False
        
    def setAtoms(self, atoms):
        
        atomArgType = getattr(atoms, '__class__', None)  # avoid to use :=
        if atomArgType:
            if atomArgType.__name__ == 'Atoms':
                self._atoms = atoms.getAtoms()
                
        self._hasAtom = True
        
    def loadTopo(self, connection):
        if connection is not None:
            if isinstance(connection, dict):
                adjDict, adjList, adjMatrix = self.__class__.validAdjDict(connection)
            elif isinstance(connection, (list, tuple)):
                adjDict, adjList, adjMatrix = self.__class__.validAdjList(connection)
            else:
                raise TypeError
            self._adjDict = adjDict
            self._adjList = adjList
            self._adjMatrix = adjMatrix

    @staticmethod
    def validAdjDict(conect):
        
        return conect, [[c, p] for c, ps in conect.items() for p in ps], None
    
    @staticmethod
    def validAdjList(conect):

        connection = defaultdict(list)
        for bond in conect:
            connection[bond[0]].append(bond[1])
            connection[bond[1]].append(bond[0])
        return dict(connection), conect, None
        
    def getBonds(self):
        
        if self._hasBond:
            return self._bonds
        
        topo = self._adjDict
        rawBonds = []
        for c, ps in topo.items():
            for p in ps:
                rawBonds.append([c, p])

        self._bonds = Bonds(rawBonds, self._atoms)
        return self._bonds
    
    def getAngles(self):
        
        if self._hasAngle:
            return self._angles

        topo = self._adjDict
        rawAngles = []
        for c, ps in topo.items():
            if len(ps) < 2:
                continue
            for (itom, ktom) in combinations(ps, 2):
                rawAngles.append([itom, c, ktom])
        self._angles = Angles(rawAngles, self._atoms)
        return self._angles
    
    def getDihedrals(self):
        
        if self._hasDihedral:
            return self._dihedrals
     
        topo = self._adjDict
        rawDihes = []
        for jtom, ps in topo.items():
            if len(ps) < 2:
                continue
            for (itom, ktom) in combinations(ps, 2):
                
                for ltom in topo[itom]:
                    if ltom != jtom:
                        rawDihes.append([ltom, itom, jtom, ktom])
                for ltom in topo[ktom]:
                    if ltom != jtom:
                        rawDihes.append([itom, jtom, ktom, ltom])
        self._dihedrals = Dihedrals(rawDihes, self._atoms)
        return self._dihedrals
    
    def getBondIdx(self):
        
        bonds = self.getBonds()
        return bonds.bondIdx
    
    def getAngleIdx(self):
        angles = self.getAngles()
        return angles.angleIdx
    
    def getDihedralIdx(self):
        dihe = self.getDihedrals()
        return dihe.dihedralIdx
    
    bonds = property(getBonds)
    angles = property(getAngles)
    dihedrals = property(getDihedrals)
    bondIdx = property(getBondIdx)
    angleIdx = property(getAngleIdx)
    dihedralIdx = property(getDihedralIdx)

    def doEmbedding(self):

        node_features = self._atoms.doEmbedding()
        jnpAdjList = jnp.array(self.adjList)
        senders = jnpAdjList[:, 0]
        receivers = jnpAdjList[:, 1]

        # edge_features = 

        # You can optionally add edge attributes to the 5 edges.
        edges = jnp.array([[5.], [6.], [7.], [8.], [8.]])

        # We then save the number of nodes and the number of edges.
        # This information is used to make running GNNs over multiple graphs
        # in a GraphsTuple possible.
        n_node = jnp.array([4])
        n_edge = jnp.array([5])

        # Optionally you can add `global` information, such as a graph label.
        global_context = jnp.array([[1]]) # Same feature dims as nodes and edges.
        graph = jraph.GraphsTuple(
            nodes=node_features,
            edges=edges,
            senders=senders,
            receivers=receivers,
            n_node=n_node,
            n_edge=n_edge,
            globals=global_context
            )
        return graph        