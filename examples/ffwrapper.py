# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-06-20
# version: 0.0.1

import xml.etree.ElementTree as ET
import xml.dom.minidom
from typing import List

parsers = {}

class SelectError(BaseException):
    pass

class Node:
    
    def __init__(self, tag, **attrs):
        
        self.tag = tag
        #TODO: self.parent = parent
        self.attrs = attrs
        self.children = []
        
    def add_child(self, child:'Node'):
        
        self.children.append(child)
        
    def add_children(self, children:List['Node']):
        self.children.extend(children)
        
    def get_children(self, key):
        return [c for c in self.children if c.tag == key]
    
    def get_child(self, key):
        for child in self.children:
            if child.tag == key:
                return child
    
    def __getitem__(self, key):
        
        return self.attrs[key]
    
    def __repr__(self):
        return f'<{self.tag}: {self.attrs}, with {len(self.children)} subnodes>'
    
    def __iter__(self):
        return iter(self.children)
    
    def __contains__(self, key):
        if self.get_child(key):
            return True
        else:
            return False


class ForcefieldTree(Node):
    def __init__(self, ):

        super().__init__('ForcefieldTree')


class XMLParser:
    def __init__(self, ffTree: ForcefieldTree):

        self.ff = ffTree
        self.difftags = []
        self.others = []

    def parse_node(self, root):

        node = Node(root.tag, **root.attrib)
        children = list(map(self.parse_node, root))
        if children:
            node.add_children(children)
        return node

    def parse(self, *xmls):

        for xml in xmls:
            root = ET.parse(xml).getroot()
            for leaf in root:
                n = self.parse_node(leaf)
                self.ff.add_child(n)
                if leaf.tag in ["AtomTypes", "Residues"]:
                    pass
                elif leaf.tag in parsers:
                    if leaf.tag not in self.difftags:
                        self.difftags.append(leaf.tag)
                else:
                    if leaf.tag not in self.others:
                        self.others.append(leaf.tag)

    def write_node(self, parent, node):
        parent = ET.SubElement(parent, node.tag, node.attrs)
        for sibiling in node:
            tmp = ET.SubElement(parent, sibiling.tag, sibiling.attrs)
            for child in sibiling:
                self.write_node(tmp, child)

    @staticmethod
    def pretty_print(element):
        initstr = ET.tostring(element, "unicode")
        pretxml = xml.dom.minidom.parseString(initstr)
        pretstr = pretxml.toprettyxml()
        return pretstr

    def write(self, path):

        root = ET.Element('Forcefield')

        for child in self.ff:
            if child.tag == 'Residues':
                Residues = ET.SubElement(root, 'Residues')
                for residue in child:
                    self.write_node(Residues, residue)
            else:
                elem = ET.SubElement(root, child.tag)
                self.write_node(elem, child)
        outstr = self.pretty_print(root)
        with open(path, "w") as f:
            f.write(outstr)


if __name__ == '__main__':

    fftree = ForcefieldTree()
    xmlParser = XMLParser(fftree)
    xmlParser.parse("test/gaff-2.11.xml", 'test/lig-prm.xml')
    xmlParser.write('test/test1.xml')

    import openmm as mm
    import openmm.app as app
    import openmm.unit as unit

    # Load topology
    app.Topology.loadBondDefinitions(f"test/lig-top.xml")
    pdb = app.PDBFile(f"test/lig.pdb")

    # Use original XML files
    ff0 = app.ForceField(f"test/gaff-2.11.xml", f"test/lig-prm.xml")
    sys0 = ff0.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff)
    integ0 = mm.VerletIntegrator(0.1)
    ctx0 = mm.Context(sys0, integ0)
    ctx0.setPositions(pdb.getPositions())
    Eref = ctx0.getState(getEnergy=True).getPotentialEnergy()

    # Use test1.xml to test reading & merging
    ff1 = app.ForceField(f"test/test1.xml")
    sys1 = ff1.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff)
    integ1 = mm.VerletIntegrator(0.1)
    ctx1 = mm.Context(sys1, integ1)
    ctx1.setPositions(pdb.getPositions())
    E1 = ctx1.getState(getEnergy=True).getPotentialEnergy()

    # Use test2.xml to test writing
    #ff2 = app.ForceField(f"{testdir}/test2.xml")
    #sys2 = ff2.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff)
    #integ2 = mm.VerletIntegrator(0.1)
    #ctx2 = mm.Context(sys2, integ2)
    #ctx2.setPositions(pdb.getPositions())
    #E2 = ctx2.getState(getEnergy=True).getPotentialEnergy()

    print("Eref:", Eref)
    print("E1:", E1)
    #print("E2:", E2)