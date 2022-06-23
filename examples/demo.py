from ffwrapper import ForcefieldTree, XMLParser, SelectError

fftree = ForcefieldTree()
xmlParser = XMLParser(fftree)

# feature 1: merge forcefield XML files
xmlParser.parse("test/gaff-2.11.xml", 'test/lig-prm.xml')
xmlParser.write('test/test1.xml')

# feature 2: get specific nodes
atomtypes = fftree.select("ForceField/AtomTypes/Type")
residues = fftree.select("ForceField/Residues/Residue")

# feature 3: get specific attributes as list
r0_charges = fftree.select("ForceField/Residues/Residue[0]/Atom<charge>")
harmonic_bond_lengths = fftree.select("ForceField/HarmonicBondForce/Bond<length>")

# feature 4: overwrite parameters
fftree.overwrite("ForceField/NonbondedForce<lj14scale>", [0.4])
fftree.overwrite("ForceField/Residues/Residue[0]/Atom<charge>", r0_charges * 0.8)
fftree.overwrite("ForceField/HarmonicBondForce/Bond<length>", harmonic_bond_lengths * 0.9)

# feature 5: raise error if the length of values and patched nodes does not match
try:
    fftree.overwrite("ForceField/Residues/Residue[0]/Atom<charge>", r0_charges[:-2])
except SelectError as e:
    print("Raise Error", e)