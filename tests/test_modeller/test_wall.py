# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-04-04
# version: 0.0.1

if __name__ == '__main__':
    
    from molpy.modeller.wall import SquareWall
    
    w = SquareWall(10, 10, 1)
    w.mesh()
    