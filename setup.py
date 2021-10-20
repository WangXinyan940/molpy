import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="molpy",
    version="0.0.1",
    author="Roy Kid",
    author_email="lijichen365@126.com",
    description="molecule data structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Roy-Kid/molpy",
    project_urls={
        "Bug Tracker": "https://github.com/Roy-Kid/molpy",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3-Clause License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)