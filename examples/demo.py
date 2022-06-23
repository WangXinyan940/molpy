from ffwrapper import ForcefieldTree, XMLParser, SelectError

fftree = ForcefieldTree()
xmlParser = XMLParser(fftree)

# feature 1: merge forcefield XML files
xmlParser.parse("test/gaff-2.11.xml", 'test/lig-prm.xml')
xmlParser.write('test/test_f1.xml')

# feature 2: get specific nodes
atomtypes = fftree.get_node("AtomTypes/Type")
residues = fftree.get_node("Residues/Residue")


# feature 3: get specific attributes as list
r0_charges = fftree.get_attrib("Residues/Residue[0]/Atom", "charge")
harmonic_bond_lengths = fftree.get_attrib("HarmonicBondForce/Bond", "length")

# feature 4: set parameters
fftree.set_attrib("NonbondedForce", "lj14scale", [0.4])
fftree.set_attrib("Residues/Residue[0]/Atom", "charge", [i * 0.8 for i in r0_charges])
fftree.set_attrib("HarmonicBondForce/Bond", "length", [i * 0.9 for i in harmonic_bond_lengths])
xmlParser.write('test/test_f4.xml')

# feature 5: set nodes
overwrite = [
    {"phase2": 3.14},
    {},
    {"phase2": 3.14, "phase3": 1.57}
]
fftree.set_node("PeriodicTorsionForce/Proper", overwrite)
xmlParser.write('test/test_f5.xml')

