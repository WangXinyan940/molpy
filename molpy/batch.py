# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-05-04
# version: 0.0.1

from collections import defaultdict
from logging import warn
from pathlib import Path
from typing import Iterable
import warnings
from molpy.system import System
import pandas as pd
from typing import List

class Batcher:
    
    def __init__(self, root_dir: str, cases_name: List[str], batch_ids: List[str], system=None, name=None):
        
        self.root_dir = root_dir
        self.cases_name = cases_name
        self.batch_ids = batch_ids
        self.name = name if name is not None else f'at {root_dir}'
        self.system = System(self.name) if system is None else system
        
    def __iter__(self):
        
        root_dir = Path(self.root_dir)
        for case_name in self.cases_name:
            for batch_id in self.batch_ids:
                fpath = root_dir / Path(case_name) / Path(batch_id)
                
                data_path = fpath / Path('data.file')
                dump_path = fpath / Path('ana.dump')
                self.system.comment = f'{case_name}_{batch_id}'
                if data_path.exists() and dump_path.exists():
                    self.system.loadData(str(data_path))
                    self.system.loadTraj(str(dump_path))
                    
                    yield self.system, batch_id
                
                else:
                    warnings.warn(f'{case_name}/{batch_id} not found')
                    
    def __repr__(self):
        return f'<Batcher: {self.name}>'
                    

class Storage:
    
    def __init__(self, name) -> None:
        
        self.name = name
        self.data = dict()
        
    def add(self, keys:Iterable, value):
        
        key = '/'.join(map(str, keys))
        if key in self.data:
            warn(f'{key} already exists')
        self.data[key] = value
        
    def get(self, keys:Iterable):
        
        key = '/'.join(keys)
        return self.data[key]
    
    def toDataFrame(self):
        df = [pd.Series(v, name=k) for k, v in self.data.items()]
        return pd.concat(df, axis=1)
    
    def to_csv(self, path=None):
        if path is None:
            path = self.name
        self.toDataFrame().to_csv(path)