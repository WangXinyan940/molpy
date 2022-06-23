import xml
import xml.etree.ElementTree as ET

modFuncs = {}


def extractHarmonicBondForce(xmlinfo):
    return {
        "Bond": {
            "length": [
                float(i["length"])
                for i in xmlinfo["Forces"]["HarmonicBondForce"]["Bond"]
            ],
            "k": [
                float(i["k"])
                for i in xmlinfo["Forces"]["HarmonicBondForce"]["Bond"]
            ]
        }
    }


def updateHarmonicBondForce(xmlinfo, xmltree):
    lengths = xmltree["HarmonicBondForce"]["Bond"]["length"]
    ks = xmltree["HarmonicBondForce"]["Bond"]["k"]
    for nit in range(len(lengths)):
        xmlinfo["Forces"]["HarmonicBondForce"]["Bond"][nit][
            "length"] = f"{lengths[nit]:.12f}"
        xmlinfo["Forces"]["HarmonicBondForce"]["Bond"][nit][
            "k"] = f"{ks[nit]:.12f}"


modFuncs["HarmonicBondForce"] = (extractHarmonicBondForce,
                                 updateHarmonicBondForce)


def extractHarmonicAngleForce(xmlinfo):
    return {
        "Angle": {
            "angle": [
                float(i["angle"])
                for i in xmlinfo["Forces"]["HarmonicAngleForce"]["Angle"]
            ],
            "k": [
                float(i["k"])
                for i in xmlinfo["Forces"]["HarmonicAngleForce"]["Angle"]
            ]
        }
    }


def updateHarmonicAngleForce(xmlinfo, xmltree):
    angles = xmltree["HarmonicAngleForce"]["Angle"]["angle"]
    ks = xmltree["HarmonicAngleForce"]["Angle"]["k"]
    for nit in range(len(angles)):
        xmlinfo["Forces"]["HarmonicAngleForce"]["Angle"][nit][
            "angle"] = f"{angles[nit]:.12f}"
        xmlinfo["Forces"]["HarmonicAngleForce"]["Angle"][nit][
            "k"] = f"{ks[nit]:.12f}"


modFuncs["HarmonicAngleForce"] = (extractHarmonicAngleForce,
                                  updateHarmonicAngleForce)


def extractPeriodicTorsionForce(xmlinfo):
    # meta is needed here for saving extra informations
    # key is periodicity
    meta = {
        "prop": {
            "prm2parser": {
                1: [],
                2: [],
                3: [],
                4: []
            },
            "parser2prm": [],
            "order": {
                1: [],
                2: [],
                3: [],
                4: []
            }
        },
        "impr": {
            "prm2parser": {
                1: [],
                2: [],
                3: [],
                4: []
            },
            "parser2prm": [],
            "order": {
                1: [],
                2: [],
                3: [],
                4: []
            }
        }
    }
    prop_phase = {1: [], 2: [], 3: [], 4: []}
    prop_k = {1: [], 2: [], 3: [], 4: []}
    for nprop, proper in enumerate(
            xmlinfo["Forces"]["PeriodicTorsionForce"]["Proper"]):
        parser2prm = []
        for key in [k for k in proper.keys() if "periodicity" in k]:
            periodicity = int(proper[key])
            period_o = int(key[-1])
            phase = float(proper[f"phase{period_o}"])
            k = float(proper[f"k{period_o}"])
            meta["prop"]["prm2parser"][periodicity].append(nprop)
            meta["prop"]["order"][periodicity].append(period_o)
            prop_phase[periodicity].append(phase)
            prop_k[periodicity].append(k)
            parser2prm.append((periodicity, len(prop_phase[periodicity]) - 1))
        meta["prop"]["parser2prm"].append(parser2prm)

    impr_phase = {1: [], 2: [], 3: [], 4: []}
    impr_k = {1: [], 2: [], 3: [], 4: []}
    for nimpr, impr in enumerate(
            xmlinfo["Forces"]["PeriodicTorsionForce"]["Improper"]):
        parser2prm = []
        for key in [k for k in impr.keys() if "periodicity" in k]:
            periodicity = int(impr[key])
            period_o = int(key[-1])
            phase = float(impr[f"phase{period_o}"])
            k = float(impr[f"k{period_o}"])
            meta["impr"]["prm2parser"][periodicity].append(nimpr)
            meta["impr"]["order"][periodicity].append(period_o)
            impr_phase[periodicity].append(phase)
            impr_k[periodicity].append(k)
            parser2prm.append((periodicity, len(impr_phase[periodicity]) - 1))
        meta["impr"]["parser2prm"].append(parser2prm)

    ret = {}
    ret["Proper"] = {"phase": prop_phase, "k": prop_k}
    ret["Improper"] = {"phase": impr_phase, "k": impr_k}
    xmlinfo["Forces"]["PeriodicTorsionForce"]["meta"] = meta
    return ret


def updatePeriodicTorsionForce(xmlinfo, xmltree):
    meta = xmlinfo["Forces"]["PeriodicTorsionForce"]["meta"]
    # prop
    for periodicity in meta["prop"]["prm2parser"].keys():
        for nterm, order in enumerate(meta["prop"]["order"][periodicity]):
            phase = xmltree["PeriodicTorsionForce"]["Proper"]["phase"][
                periodicity][nterm]
            k = xmltree["PeriodicTorsionForce"]["Proper"]["k"][periodicity][
                nterm]
            parseridx = meta["prop"]["prm2parser"][periodicity][nterm]
            xmlinfo["Forces"]["PeriodicTorsionForce"]["Proper"][parseridx][
                f"phase{order}"] = phase
            xmlinfo["Forces"]["PeriodicTorsionForce"]["Proper"][parseridx][
                f"k{order}"] = k

    # impr
    for periodicity in meta["impr"]["prm2parser"].keys():
        for nterm, order in enumerate(meta["impr"]["order"][periodicity]):
            phase = xmltree["PeriodicTorsionForce"]["Improper"]["phase"][
                periodicity][nterm]
            k = xmltree["PeriodicTorsionForce"]["Improper"]["k"][periodicity][
                nterm]
            parseridx = meta["impr"]["prm2parser"][periodicity][nterm]
            xmlinfo["Forces"]["PeriodicTorsionForce"]["Improper"][parseridx][
                f"phase{order}"] = phase
            xmlinfo["Forces"]["PeriodicTorsionForce"]["Improper"][parseridx][
                f"k{order}"] = k


modFuncs["PeriodicTorsionForce"] = (extractPeriodicTorsionForce,
                                    updatePeriodicTorsionForce)


def extractNonbondedForce(xmlinfo):
    keys = [
        k for k in xmlinfo["Forces"]["NonbondedForce"]["Atom"][0].keys()
        if "class" not in k and "type" not in k
    ]
    ret = {
        'coulomb14scale': [
            float(xmlinfo["Forces"]["NonbondedForce"]["attributes"]
                  ["coulomb14scale"])
        ],
        'lj14scale': [
            float(
                xmlinfo["Forces"]["NonbondedForce"]["attributes"]["lj14scale"])
        ],
        "Atom": {}
    }
    for key in keys:
        ret["Atom"][key] = [
            float(i[key]) for i in xmlinfo["Forces"]["NonbondedForce"]["Atom"]
        ]
    return ret


def updateNonbondedForce(xmlinfo, xmltree):
    # update 14scale
    coul14 = xmltree["NonbondedForce"]["coulomb14scale"][0]
    xmlinfo["Forces"]["NonbondedForce"]["attributes"][
        "coulomb14scale"] = f"{coul14:.12f}"
    lj14 = xmltree["NonbondedForce"]["lj14scale"][0]
    xmlinfo["Forces"]["NonbondedForce"]["attributes"][
        "lj14scale"] = f"{lj14:.12f}"
    keys = [
        k for k in xmlinfo["Forces"]["NonbondedForce"]["Atom"][0].keys()
        if "class" not in k and "type" not in k
    ]
    if len(keys) == 0:
        return
    for natom in range(len(xmltree["NonbondedForce"]["Atom"][keys[0]])):
        for key in keys:
            val = xmltree["NonbondedForce"]["Atom"][key][natom]
            xmlinfo["Forces"]["NonbondedForce"]["Atom"][natom][
                key] = f"{val:.12f}"


modFuncs["NonbondedForce"] = (extractNonbondedForce, updateNonbondedForce)


def extractParameter(xmlinfo):
    xmltree = {}
    # work on residues
    xmltree["Residues"] = []
    attribs = []
    for key in xmlinfo["Residues"][0]["Atom"][0].keys():
        if key not in ["name", "type"]:
            attribs.append(key)
    for res in xmlinfo["Residues"]:
        ret = {}
        for attr in attribs:
            ret[attr] = [float(i[attr]) for i in res["Atom"]]
        xmltree["Residues"].append(ret)
    # work on forces
    for fname in modFuncs.keys():
        xmltree[fname] = modFuncs[fname][0](xmlinfo)
    return xmltree


def updateParameter(xmlinfo, xmltree):
    # work on residues
    for nres in range(len(xmltree["Residues"])):
        for attr in xmltree["Residues"][nres].keys():
            for natom in range(len(xmltree["Residues"][nres][attr])):
                val = xmltree["Residues"][nres][attr][natom]
                xmlinfo["Residues"][nres]["Atom"][natom][attr] = f"{val:.12f}"
    # work on forces
    for fname in modFuncs.keys():
        modFuncs[fname][1](xmlinfo, xmltree)


def parseNode(root):
    ret = {"attributes": root.attrib}
    for child in root:
        if child.tag not in ret:
            ret[child.tag] = []
        ret[child.tag].append(child.attrib)
    return ret


def readForceField(*args):
    xmlinfo = {"AtomTypes": [], "Residues": [], "Forces": {}, "Others": {}}
    for xmlfile in args:
        root = ET.parse(xmlfile).getroot()
        for nodeL1 in root:
            if nodeL1.tag == "AtomTypes":
                xmlinfo["AtomTypes"] = parseNode(nodeL1)
            elif nodeL1.tag == "Residues":
                for child in nodeL1:
                    xmlinfo["Residues"].append(parseNode(child))
            elif nodeL1.tag in modFuncs:
                xmlinfo["Forces"][nodeL1.tag] = parseNode(nodeL1)
            else:
                xmlinfo["Others"][nodeL1.tag] = parseNode(nodeL1)
    return xmlinfo


def writeNode(name, node, f, left="    "):
    f.write(f'{left}<{name}')
    for k, v in node["attributes"].items():
        f.write(f' {k}="{v}"')
    f.write(">\n")
    for tag in node.keys():
        if tag == "attributes" or tag == "meta":
            continue
        for item in node[tag]:
            f.write(f'{left}    <{tag}')
            for k, v in item.items():
                f.write(f' {k}="{v}"')
            f.write("/>\n")
    f.write(f'{left}</{name}>\n')


def writeForceField(filename, xmlinfo):
    with open(filename, "w") as f:
        # write head
        f.write("<ForceField>\n")
        # write AtomTypes
        writeNode("AtomTypes", xmlinfo["AtomTypes"], f, left="    ")
        # write Residues
        f.write("    <Residues>\n")
        for elem in xmlinfo["Residues"]:
            writeNode("Residue", elem, f, left="        ")
        f.write("    </Residues>\n")
        # write readable forces
        for force in xmlinfo["Forces"]:
            writeNode(force, xmlinfo["Forces"][force], f, left="    ")
        # write others
        for item in xmlinfo["Others"]:
            writeNode(item, xmlinfo["Others"][item], f, left="    ")
        # write end
        f.write("</ForceField>")


if __name__ == "__main__":
    import openmm as mm
    import openmm.app as app
    import openmm.unit as unit

    # Generate test files
    testdir = "test"
    xmlinfo = readForceField(f"{testdir}/gaff-2.11.xml",
                             f"{testdir}/lig-prm.xml")
    writeForceField(f"{testdir}/test1.xml", xmlinfo)
    xmltree = extractParameter(xmlinfo)
    updateParameter(xmlinfo, xmltree)
    writeForceField(f"{testdir}/test2.xml", xmlinfo)

    # Load topology
    app.Topology.loadBondDefinitions(f"{testdir}/lig-top.xml")
    pdb = app.PDBFile(f"{testdir}/lig.pdb")

    # Use original XML files
    ff0 = app.ForceField(f"{testdir}/gaff-2.11.xml", f"{testdir}/lig-prm.xml")
    sys0 = ff0.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff)
    integ0 = mm.VerletIntegrator(0.1)
    ctx0 = mm.Context(sys0, integ0)
    ctx0.setPositions(pdb.getPositions())
    Eref = ctx0.getState(getEnergy=True).getPotentialEnergy()

    # Use test1.xml to test reading & merging
    ff1 = app.ForceField(f"{testdir}/test1.xml")
    sys1 = ff1.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff)
    integ1 = mm.VerletIntegrator(0.1)
    ctx1 = mm.Context(sys1, integ1)
    ctx1.setPositions(pdb.getPositions())
    E1 = ctx1.getState(getEnergy=True).getPotentialEnergy()

    # Use test2.xml to test writing
    ff2 = app.ForceField(f"{testdir}/test2.xml")
    sys2 = ff2.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff)
    integ2 = mm.VerletIntegrator(0.1)
    ctx2 = mm.Context(sys2, integ2)
    ctx2.setPositions(pdb.getPositions())
    E2 = ctx2.getState(getEnergy=True).getPotentialEnergy()

    print("Eref:", Eref)
    print("E1:", E1)
    print("E2:", E2)