# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-01-07
# version: 0.0.2

import freud

class Box(freud.Box):
    
    def __repr__(self):
        return ("molpy.box.{cls}(Lx={Lx}, Ly={Ly}, Lz={Lz}, "
                "xy={xy}, xz={xz}, yz={yz}, "
                "is2D={is2D})").format(cls=type(self).__name__,
                                       Lx=self.Lx,
                                       Ly=self.Ly,
                                       Lz=self.Lz,
                                       xy=self.xy,
                                       xz=self.xz,
                                       yz=self.yz,
                                       is2D=self.is2D)