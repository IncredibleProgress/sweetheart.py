"""
sws utilities for testing webapp 
"""

from sweetheart import __version__
assert __version__ == '0.1.2'

import os,shutil
from sweetheart.subprocess import *
#from sweetheart.sweet import *
from sweetheart.services import *
from sweetheart.install import *


def symlink(source,dest):

    if os.path.islink(dest): print(f"Warning, existing link {dest}")
    elif os.path.isfile(dest): os.remove(dest)
    elif os.path.isdir(dest) : shutil.rmtree(dest)
    try: os.symlink(source,dest)
    except: pass

def _dev_links_():

    src = f"{BaseConfig.HOME}/{MASTER_MODULE}.py"# source dir
    pjt = f"{BaseConfig.HOME}/.sweet/{MASTER_MODULE}"# project dir

    # make links for testing dev files
    symlink(f"{src}/configuration/packages.json",f"{pjt}/configuration/packages.json")
    symlink(f"{src}/webpages/resources/tailwind.base.css",f"{pjt}/webpages/resources/tailwind.base.css")
    symlink(f"{src}/webpages/resources/tailwind.config.js",f"{pjt}/webpages/resources/tailwind.config.js")
    symlink(f"{src}/webpages/HTML",f"{pjt}/webpages/HTML")

    # make links for testing dev directories
    symlink(f"{src}/webpages/templates",f"{pjt}/webpages/templates")
    symlink(f"{src}/documentation/sweetbook",f"{pjt}/documentation/sweetbook")
    symlink(f"{src}/documentation/notebooks",f"{pjt}/documentation/notebooks")

def _dev_sweetheart_():
    # link ~/sweetheart.py as python package
    set_config()
    sp.poetry("remove","sweetheart")

    symlink(f"{BaseConfig.HOME}/{MASTER_MODULE}.py",
        f"{BaseConfig._.python_env}/lib/python*/site-packages/sweetheart")


def test_template(template:str):
    
    BaseConfig.verbosity = 1
    config = set_config({})
    config.is_webapp_open = True
    config.is_rethinkdb_local = False
    config.is_jupyter_local = False

    # force re-building tailwind.css
    echo("build generic tailwindcss file")
    sp.shell(config.subproc['.tailwindcss'],cwd=f"{config.root_path}/webpages/resources")

    path = f"{config['working_dir']}/{config['templates_dir']}"
    if not os.path.isfile(path) and not os.path.islink(path):
        print("Error, the given template is not existing")
        return False

    webapp = HttpServer(config,set_database=False).mount(
        Route("/",HTMLTemplate(template)) )

    quickstart(webapp)
    return True


if __name__ == '__main__':

    from sys import argv

    if '--dev-sweetheart' in argv:
        _dev_sweetheart_()
        echo("replace sweetheart module with dev module: all done")

    if '--dev-links' in argv: 
        _dev_links_()
        echo("create symbolic links for dev: all done")

    if not argv[-1].startswith("-"):
        assert test_template(argv[-1])
