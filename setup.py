# author: Roy Kid
# contact: lijichen365@126.com
# date: 2022-04-04
# version: 0.0.1

from skbuild import setup as skbuild_setup

version = "0.0.1"

description = "molpy"

readme = "test"

def setup(*args, **kwargs):
    
    skbuild_setup(*args, **kwargs)
    
    
setup(
    name='molpy',
    version=version,
    packages=['molpy'],
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=(
        'analysis'
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        # "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: C++",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
    maintainer="Roy Kid",
    maintainer_email="lijichen365@126.com",
    author="Roy Kid",
    author_email="lijichen365@126.com",
    url="https://github.com/Roy-Kid/molpy",
    download_url="https://pypi.org/project/molpy/",
    project_urls={
        "Homepage": "https://github.com/Roy-Kid/molpy",
        "Documentation": "https://molpy.readthedocs.io/",
        "Source Code": "https://github.com/Roy-Kid/molpy",
        "Issue Tracker": "https://github.com/Roy-Kid/molpy/issues",        
    },
    python_requires=">=3.6",
    install_requires=[
        "cython>=0.29.14",
        "numpy>=1.14",
    ],
    test_requires=[
        "pytest>=5.4.1",    
    ],
)
