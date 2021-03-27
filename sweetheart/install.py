
from sweetheart.globals import *


PKG_INIT = { 
    'pylibs': ["bottle","pymongo","uvicorn","aiofiles","starlette","jupyterlab"],
    'aptlibs': ["xterm","rustc","mongodb","npm"],
    'cargolibs': ["mdbook","mdbook-toc"],
    'npmlibs': ["brython","d3"] }


def init(config:BaseConfig):
    """ set require configuration before sweetheart installation
        and intends to provide minimalistic sweetheart features """

    # require directories
    for basedir in [
        f"{config.root_path}/configuration",
        f"{config.root_path}/database",
        f"{config.root_path}/documentation/notebooks",
        f"{config.root_path}/programs/scripts",
        f"{config.root_path}/webpages/resources",
        f"{config.root_path}/webpages/markdown",
        f"{config.root_path}/webpages/{config['templates_dir']}",
    ]: os.makedirs(basedir,exist_ok=True)

    # provide default libs
    config.subproc.update(PKG_INIT)

    # require python-poetry
    if not os.path.isfile(config.poetry_bin):
        sp.shell("curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -")
    
    # set path and name for new poetry python package
    path,name = os.path.split(config.subproc['codepath'])
    assert name != ""

    # provide default python package and venv
    os.makedirs(path,exist_ok=True)
    os.chdir(path)
    sp.poetry("-q","new",name)
    sp.set_python_env(path=config.subproc['codepath'])

    # install default libs
    installer = BaseInstall(config)
    installer.install_libs()

    # provide installed javascript libs (Ubuntu)
    os.symlink("/usr/share/javascript",
        f"{config.root_path}/webpages/resources/javascript")


class BaseInstall:

    def __init__(self,config:BaseConfig) -> None:
        self.config = config

    def apt(self,libs:list,**kwargs):
        """ install distro packages using apt """

        echo("apt install",*libs,"...")
        return sp.run("sudo","apt","install",*libs,**kwargs)

    def cargo(self,libs:list,**kwargs):
        """ install rust crates using cargo """

        echo("cargo install",*libs,"...")
        path = self.config.subproc['rustpath']
        return sp.run(f"{path}/cargo","install",*libs,**kwargs)
    
    def poetry(self,libs:list,**kwargs):
        """ install python packages using poetry """

        echo("poetry add python modules",*libs,"...")
        os.chdir(self.config.subproc['codepath'])
        return sp.poetry("add",*libs,**kwargs)

    def npm(self,libs:list,init=False,**kwargs):
        """ install node modules using npm """

        echo("npm install",*libs,"...")
        os.chdir(f"{self.config.root_path}/webpages/resources")
        if init: sp.run("npm","init","--yes")
        return sp.run("npm","install",*libs,**kwargs)

    def install_libs(self,libs:dict=None,init=False):
        """ install given libs using apt,cargo,poetry,npm 
            no given libs will set init process for new project 
            and install libs provided within config.subproc """

        if libs is None:
            init = True
            libs = PKG_INIT

        aptlibs = libs.get('aptlibs')
        if aptlibs: self.apt(aptlibs)

        cargolibs = libs.get('cargolibs')
        if cargolibs: self.cargo(cargolibs)

        pylibs = libs.get('pylibs')
        if pylibs: self.poetry(pylibs)

        npmlibs = libs.get('npmlibs')
        if npmlibs: self.npm(npmlibs,init)

