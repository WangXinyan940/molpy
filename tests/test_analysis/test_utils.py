# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-02-20
# version: 0.0.1

from functools import partial
from molpy.analysis.utils import Accumulator, Reducer
from operator import mul, add
import numpy as np

single_value = np.arange(5) + 1

class TestAccumulator:
    
    def test_init(self):
        mul_acc = Accumulator(mul, 'test_mul')
        for i in single_value:
            mul_acc(i)
        assert mul_acc.value == 120
        
    
    def test_partial(self):
        p_add_acc = partial(Accumulator, add)
        add_acc = p_add_acc('test_add')
        for i in single_value:
            add_acc(i)
        assert add_acc.value == 15
        
    
class TestReducer:
    
    def test_init(self):
        mul_red = Reducer(mul, 'test_mul')
        assert mul_red(single_value).value == 120
        
    def test_partial(self):
        p_add_red = partial(Reducer, add)
        add_red = p_add_red('test_add')
        assert add_red(single_value).value == 15