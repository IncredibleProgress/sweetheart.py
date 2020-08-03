from setuptools import setup

setup(
    name="sweetheart",
    version= "0.1.dev5",
    license= "CeCILL-C",
    packages=[""],

    # metadata to display on PyPI
    author="Nicolas Champion",
    author_email="champion.nicolas@gmail.com",
    description="a supercharged heart for the non-expert hands",
    long_description = """
sweetheart.py
=============

Since Ubuntu 20.04 can be installed as usual softwares within windows 10, it provides an incredible way for any organization to develop, administrate, deploy powerfull webapps on its own local network and giving high capabilities of integration with already existing tools. Sweetheart will propose a simple and efficient approach to do it leading you to the best coding practices.

sweetheart provides highest quality components and aims to be adopted by newbies:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- easy to learn, easy to use
- full documentation provided
- quick and clean prototyping
- quick and clean deployement
- ready for maintenable great code quality
- ready for datacenters, big-data and ai
- ready for inovation and creativity

sweetheart is python/html/css centric meaning that you can do a lot by yourself and you will find support and skilled people everywhere for lowest costs (e.g. projects with studients)

sweetheart provides supercharged basis available for your non-expert hands:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- provided database server: MongoDB
- provided webservers: Uvicorn, CherryPy
- responsive user interfaces: Html
- backend language: Python3
- frontend language: Typescript
- provided libs for going fast: Knacss, W3css
- provided libs for high-level featuring: Bootstrap4, Vue.js
- all others nice things you wish using apt, pip and npm
    """,

    keywords="ubuntu mongodb starlette webapp industry4.0",
    plateformes = "Ubuntu 20.04",

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