from setuptools import setup, find_packages
import molpy as mp

meta_data = {
    'name': mp.NAME,
    'version': mp.VERSION,
    'author': mp.AUTHOR,
    'author_email': mp.AUTHOR_EMAIL,
    'description': mp.DISCRIPTION,
    'packages': find_packages(),
}


setup(
    **meta_data
)