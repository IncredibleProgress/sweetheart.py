import os
from setuptools import setup

readme = os.path.join(os.getcwd(),"README.md")
with open(readme) as file:
    long_description = file.read()

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
    long_description = long_description,
    long_description_content_type = "text/markdown",

    keywords="ubuntu mongodb starlette webapp industry4.0",
    # url="http://",
    project_urls={
        # "Bug Tracker": "https://",
        # "Documentation": "https://",
        "Source Code": "https://github.com/IncredibleProgress/sweetheart.py",
    },

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