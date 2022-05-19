from setuptools import setup, find_packages
import molpy as mp
from glob import glob
from pybind11.setup_helpers import Pybind11Extension

meta_data = {
    'name': mp.NAME,
    'version': mp.VERSION,
    'author': mp.AUTHOR,
    'author_email': mp.AUTHOR_EMAIL,
    'description': mp.DISCRIPTION,
    'packages': find_packages(),
}

ext_modules = [
    
    Pybind11Extension(
        'molpy_cpp',
        glob('cpp/src/*.cpp') + glob('cpp/*.cpp'),
        define_macros=[('VERSION_INFO', mp.VERSION)],
        include_dirs=['cpp/include'],
    )  # delete build folder before rebuild
]

setup(
    **meta_data,
    ext_modules=ext_modules,
)