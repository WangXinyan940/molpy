# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-03-12
# version: 0.0.1

from molpy.io.fileHandler import FileHandler
import pytest


class TestFileHandler:
    
    @pytest.fixture(scope='class', name='dump')
    def test_init(self):
        
        fpath = 'tests/data/linear.dump'
        
        handler = FileHandler(fpath)
        
        yield handler
        
    def test_jump(self, dump):
        
        pass
    
    def test_readlines(self, dump):
        
        assert dump.readlines()[0] == 'ITEM: TIMESTEP\n'
        assert len(dump.readlines()) == 759
        
    def test_iter(self, dump):
        
        dump.reset_fp()
        l = list(dump)
        assert len(l) == 759
        l = list(dump)
        assert len(l) == 0
    
    def test_getline(self, dump):
        
        assert dump.getline(1) == 'ITEM: TIMESTEP\n'
        assert dump.getline(700) == '36 9 6 -11.8 43.4288 44.4385 2.92884\n'
    
    def test_readchunk(self, dump):
        
        chunks = dump.readchunks('ITEM: TIMESTEP')
    
        assert chunks.nchunks == 11
        
class TestChunks:
    
    @pytest.fixture(scope='class', name='chunks')
    def test_init(self):
        
        fpath = 'tests/data/linear.dump'
        
        handler = FileHandler(fpath)
        
        chunks = handler.readchunks('ITEM: TIMESTEP')
        
        yield chunks

    def test_nchunks(self, chunks):
        
        assert chunks.nchunks == 11
        
    def test_getChunk(self, chunks):
        
        assert chunks.isScan
        
        chunk = chunks[2]
        
        line = chunk[1]
        assert int(line) == 20
        line = chunk[-1]
        assert line == '45 18 6 -11.8 2.37502 43.1304 46.726'
        

        