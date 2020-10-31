import os
from sweet import __version__, __license__
from setuptools import setup

readme = os.path.join(os.getcwd(),"README.md")
with open(readme) as file:
    long_description = file.read()

setup(
    name="sweetheart",
    version= __version__,
    license= __license__,
    #setup_requires= [""],
    #packages=[""],
    scripts=["sweet.py"],

    # metadata to display on PyPI
    author="Nicolas Champion",
    author_email="champion.nicolas@gmail.com",
    description="build at the speedlight full-stacked webapps including AI",
    long_description = long_description,
    long_description_content_type = "text/markdown",

    keywords="ubuntu rust python3 mongodb webapp machinelearning industry4.0",
    # url="http://",
    project_urls={
        # "Bug Tracker": "https://",
        "Documentation": "https://filedn.eu/l2gmEvR5C1WbxfsrRYz9Kh4/sweetbook/",
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