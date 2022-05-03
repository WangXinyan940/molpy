
from molpy.system import System


data_dir = '/home/roy/work/duan/1/data.file'
dump_dir = '/home/roy/work/duan/1/eq.dump'

system = System('test')
atoms = system.loadData(data_dir)
traj = system.loadTraj(dump_dir)
system.selectFrame(1)

