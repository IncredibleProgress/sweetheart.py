from setuptools import setup

setup(
    name="sweetheart",
    version= "0.1.dev6",
    license= "CeCILL-C",
    packages=[""],
    scripts=["sweet.py"],

    # metadata to display on PyPI
    author="Nicolas Champion",
    author_email="champion.nicolas@gmail.com",
    description="a supercharged heart for the non-expert hands",

    keywords="ubuntu mongodb starlette webapp industry4.0",
    # url="http://example.com/HelloWorld/",
    project_urls={
        # "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        # "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://github.com/IncredibleProgress/sweetheart.py",
    },

    long_description = """
=============
sweetheart.py
=============

Sweetheart propose a simple approach for buiding webapps leading you to the best coding practices.

It runs on Ubuntu 20.04 LTS and Windows10 through the WSL.

sweetheart provides highest quality components and aims to be adopted by newbies:
`````````````````````````````````````````````````````````````````````````````````
- easy to learn, easy to use
- full documentation provided
- quick and clean prototyping
- quick and clean deployement
- ready for maintenable great code quality
- ready for datacenters, big-data and ai
- ready for inovation and creativity

sweetheart provides a supercharged heart for the non-expert hands:
``````````````````````````````````````````````````````````````````
- provided database server: MongoDB
- provided webservers: Uvicorn, CherryPy
- responsive user interfaces: Html
- backend language: Python3
- frontend language: Typescript
- provided libs for going fast: Knacss, W3css
- provided libs for high-level featuring: Bootstrap4, Vue.js
- all others nice things you wish using apt, pip and npm
    """,

    classifiers = [
        "Environment :: Web Environment",
        "Intended Audience :: Manufacturing",
        "License :: CeCILL-C Free Software License Agreement (CECILL-C)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: System :: Installation/Setup" ]
)