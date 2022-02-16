from molpy.packmol import PackmolWithJax
import jax.numpy as jnp

class TestPackmol:

    def test_packmol(self):
        packmol = PackmolWithJax()
        mol = jnp.array([[[0,0,0],[1,0,0]], [[0,1,0],[1,1,0]]])
        packmol.loadMolecules(mol)
        packmol.initThetas()
        packmol.apply(10)
        print(packmol.atoms)