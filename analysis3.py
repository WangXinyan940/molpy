from functools import partial
from operator import add
import numpy as np
import molpy as mp
from molpy.analysis import diffraction, density, cluster
from tqdm import tqdm
import csv
from molpy.analysis.analysis import AnalysisTaskManagement, Analyzer
from molpy.analysis.utils import Accumulator

from molpy.utils import PathUtils
from pathlib import Path
        
class PaperAnalyzer(Analyzer):
    
    def __init__(self, name, path, isSave=False):
        super().__init__(name)
        self._name = name
        if isinstance(path, Path):
            self._dataDir = path
        else:
            self._dataDir = Path(path)
        self.isSave = isSave
        self.__post_init__()
        
    def __post_init__(self):
        # init kernel

        # calc group-ion
        self.rdfKernel0 = density.RDF(bins=200, r_max=24, r_min=0)
        # calc 
        self.rdfKernel1 = density.RDF(bins=200, r_max=24, r_min=0)
        # calc
        self.rdfKernel2 = density.RDF(bins=200, r_max=24, r_min=0)

        self.sqKernel = diffraction.StaticStructureFactorDirect(bins=100, k_max=10, k_min=0)
        self.clusterKernel = cluster.Cluster()   
        self.cl_props = cluster.ClusterProperties()
        
        add_accumulator = partial(Accumulator, add)
        self.gyration_tensor_acc = add_accumulator('gy_tensor')
        self.rg_acc = add_accumulator('rg')
        self.asphericity_acc = add_accumulator('asphericity')
        self.prolateness_acc = add_accumulator('prolateness')
        
                
    def check(self):
        if len(list(self._dataDir.glob('*3e6.data'))) == 0:
            return 'not complete'
        
    def open(self):
        dataName = Path(self._dataDir.stem)
        
        self.system = mp.System()
        try:
            self.system.loadData(self._dataDir/dataName.with_suffix('.data'))        
            self.system.loadTraj(self._dataDir/dataName.with_suffix('.dump'))
        except:
            return 'not found'
        
    def ensemble_average(self):
        nframes = self.system.nframes
        for nframe in tqdm(range(1000, nframes)):
            self.one(nframe)
                
    def one(self, nframe):
        
        self.system.selectFrame(nframe)
        self.system.atoms.mergeFields(['x', 'y', 'z'], 'position')
        fields = self.system.getAtomsStructuredArray()
        box = self.system.box
        
        # packing
        allPos = fields['position']
        poly = fields[fields['type']<4]
        poly_pos = poly['position']
        
        io_backbone = fields[fields['type']==1]
        io_group = fields[fields['type']==3]
        io_counterion = fields[fields['type']==4]

       
        io_backbone_pos = io_backbone['position']
        io_group_pos = io_group['position']
        io_counterion_pos = io_counterion['position']

        pe = fields[fields['type']==2]
        pe_pos = pe['position']

        # calc RDF
        self.rdfKernel0.compute((box, io_group_pos), query_points=io_counterion_pos, reset=False)

        # cluster
        self.clusterKernel.compute((box, io_backbone_pos), neighbors=dict(r_max=1.5))
        
        self.cl_props.compute((box, io_backbone_pos), self.clusterKernel.cluster_idx, )
        COM = self.cl_props.centers

        self.rdfKernel1.compute((box, COM), query_points=io_backbone_pos, reset=False)  # COM-io

        self.rdfKernel2.compute((box, COM), query_points=pe_pos, reset=False)  # COM-pe
        
        self.gyration_tensor_acc(self.cl_props.gyrations)
        self.rg_acc(self.cl_props.radii_of_gyration)
        self.asphericity_acc(self.cl_props.asphericity)
        self.prolateness_acc(self.cl_props.prolateness)
        
    def after(self):
        
        fields = self.system.getAtomsStructuredArray()
        box = self.system.box
        io = fields[np.logical_or(fields['type']==1 , fields['type']==3)]
        io_pos = io['position']
        # self.sqKernel.compute((box, io_pos), reset=True)
        
        self.clusterKernel.compute((box, io_pos), neighbors=dict(r_max=1.5))
        self.cl_props.compute((box, io_pos), self.clusterKernel.cluster_idx)
        
        # single value
        self.data['test'] = 'test'
        self.data['gyration_tensor'] = self.cl_props.gyrations
        self.data['Rg'] = self.cl_props.radii_of_gyration
        self.data['asphericity'] = self.cl_props.asphericity
        self.data['prolateness'] = self.cl_props.prolateness
        self.data['size'] = np.array(list(map(len, self.clusterKernel.cluster_keys)))
        self.data['num_cluster'] = self.clusterKernel.num_clusters
        
        delattr(self, 'rdfKernel0')
        delattr(self, 'rdfKernel1')
        delattr(self, 'rdfKernel2')
        delattr(self, 'cl_props')
        delattr(self, 'clusterKernel')
        delattr(self, 'sqKernel')
  
    def start(self):

        self.open()
        self.check()
        # self.before()
        self.ensemble_average()
        self.after()

    def __call__(self, *args, **kwds):
        self.start()
        return self
        

if __name__ == '__main__':
    
    # aq = mp.AnalysisQueue()
    
    rootDir = Path('/home/lijichen/work/duan/paper')
    mode = Path('mode1')
    # 1. check if exists; 
    # 2. return list
    dataDir = list((rootDir/mode).glob('io*'))
    am = AnalysisTaskManagement()

    for test_sample in dataDir:
        a = PaperAnalyzer(f"{test_sample.stem}", test_sample, isSave=True)
        am.newTask(a, )
    
    analyzers = am.retrive(block=True)
    
    save = True
    if save:
        header = []
        for analyzer in analyzers:
            header.append(analyzer.name)
        # single value
        gyraion_tensor = []
        rg = []
        asphericity = []
        prolatenesss = []
        size = []
        for analyzer in analyzers:
            
            print(analyzer.gyration_tensor_acc.value)
            
            # gyraion_tensor.append(analyzer.data['gyration_tensor'])
            # rg.append(analyzer.data['Rg'])
            # asphericity.append(analyzer.data['asphericity'])
            # prolatenesss.append(analyzer.data['prolateness'])
            # size.append(analyzer.data['size'])
                        
        
        # res = np.vstack([rg, asphericity, prolatenesss, size]).T
        
        # with open('asphericity.txt', 'w') as f:
        #     for i in range(len(header)):
        #         f.write(f'{header[i]} {" ".join(map(lambda x: str(round(x, 4)), asphericity[i]))}\n')
                
        # with open('prolateness.txt', 'w') as f:
        #     for i in range(len(header)):
        #         f.write(f'{header[i]} {" ".join(map(lambda x: str(round(x, 4)), prolatenesss[i]))}\n')      
                
        # with open('rg.txt', 'w') as f:
        #     for i in range(len(header)):
        #         f.write(f'{header[i]} {" ".join(map(lambda x: str(round(x, 2)), rg[i]))}\n')  