
from sweetheart.globals import *
from sweetheart.sweet import *
from sweetheart.heart import *
from sweetheart.install import *

from sweetheart import __version__
assert __version__ == '0.1.1'

def test_init():
    init(config=set_config(project="test"))
    sp.shell("rm -r ~/.sweet/test")

def test_objects():

    try:
        config = set_config(sandbox=False)
        RethinkDB(config)
        JupyterLab(config)
        HttpServer(config)
        return True

    except:
        return False

def test_template(template:str):
    
    BaseConfig.verbosity = 1
    config = set_config({'webbrowser':"brave.exe"})
    config.is_rethinkdb_local = True
    config.is_webapp_open = True

    path = f"{config['working_dir']}/{config['templates_dir']}"
    if not os.path.isfile(path) and not os.path.islink(path):
        print("Error, the given template is not existing")
        return False

    webapp = HttpServer(config).mount(
        Route("/",HTMLTemplate(template)) )

    quickstart(webapp)
    return True


def _set__links_for_dev_():

    import os,shutil
    src = f"{BaseConfig.HOME}/{MASTER_MODULE}.py"# source dir
    pjt = f"{BaseConfig.HOME}/.sweet/{MASTER_MODULE}"# project dir

    def symlink(source,dest):
        if os.path.islink(dest): print(f"Warning, existing link {dest}")
        elif os.path.isfile(dest): os.remove(dest)
        elif os.path.isdir(dest) : shutil.rmtree(dest)
        try: os.symlink(source,dest)
        except: pass

    # make links for testing dev files
    symlink(f"{src}/configuration/packages.js",f"{pjt}/configuration/packages.js")
    symlink(f"{src}/webpages/resources/tailwind.base.css",f"{pjt}/webpages/resources/tailwind.base.css")
    symlink(f"{src}/webpages/resources/tailwind.config.js",f"{pjt}/webpages/resources/tailwind.config.js")
    symlink(f"{src}/webpages/HTML",f"{pjt}/webpages/HTML")

    # make links for testing dev directories
    symlink(f"{src}/webpages/templates",f"{pjt}/webpages/templates")
    symlink(f"{src}/documentation/sweetbook",f"{pjt}/documentation/sweetbook")
    symlink(f"{src}/documentation/notebooks",f"{pjt}/documentation/notebooks")


if __name__ == '__main__':

    from sys import argv

    if '--init' in argv:
        test_init()
        echo("sws test --init: all done",mode='exit')

    elif '--dev-links' in argv: 
        _set__links_for_dev_()
        echo("sws test --dev-links: all done",mode='exit')
    
    #assert test_objects()
    assert test_template(argv[-1])
