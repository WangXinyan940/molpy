# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-04-04
# version: 0.0.1

cimport molpy.modeller.wall as wall

cdef class SquareWall:

    cdef wall.SquareWall * thisptr

    def __cinit__(self, lx, ly, nlayer=1):

        self.thisptr = new wall.SquareWall(lx, ly, nlayer)

    def __dealloc__(self):
        del self.thisptr