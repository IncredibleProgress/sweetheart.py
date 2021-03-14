
import os,subprocess
from sweetheart.globals import *


class sp:
    """ namespace providing basic subprocess features """

    run = lambda *args,**kwargs: subprocess.run(args,**kwargs)
    shell = lambda str,**kwargs: subprocess.run(str,**kwargs,shell=True)

    @classmethod
    def poetry(cls,*args,**kwargs):
        return cls.run(BaseConfig.poetry_bin,*args,**kwargs)

    @classmethod
    def python(cls,*args,**kwargs):
        return cls.run(BaseConfig.python_bin,*args,**kwargs)

    @classmethod
    def set_python_env(cls,path:str):
        """ get python venv path from poetry and set it within config
            beware: path must exist and contain a poetry project """

        os.chdir(path)
        run = cls.poetry("env","info","--path",text=True,capture_output=True)
        assert run.returncode == 0
        BaseConfig.python_bin = f"{run.stdout}/bin/python"
    

def init(config:BaseConfig):
    """ set require configuration before sweetheart installation
        and intends to provide minimalistic sweetheart features """

    # require directories
    for basedir in [
        f"{config.root_path}/configuration",
        f"{config.root_path}/database",
        f"{config.root_path}/documentation",
        f"{config.root_path}/programs",
        f"{config.root_path}/webpages",
        f"{config.root_path}/webpages/{config['templates_dir']}",
    ]: os.mkdir(basedir)

    # provide default libs
    config.subproc.update({
        'aptlibs': ["xterm","rustc","mongodb","npm"],
        'pylibs': ["pymongo","uvicorn","starlette","jupyterlab"],
        'cargolibs': ["mdbook","mdbook-toc"],
        'npmlibs': [],})

    # require python-poetry
    if not os.path.isfile(config.poetry_bin):
        echo("installation of python-poetry required")
        sp.shell("curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -")
    
    # set path and name for new poetry python package
    path,name = os.path.split(config.subproc['codepath'])
    assert name != ""

    # provide default python package and venv
    os.makedirs(path,exist_ok=True)
    os.chdir(path)
    sp.poetry("-q","new",name)
    sp.set_python_env(config.subproc['codepath'])

    # install default libs
    installer = BaseInstall(config)
    installer.install_libs()

    os.symlink("/usr/share/javascript",
        f"{config.root_path}/webpages/javascript_libs")


class BaseInstall:

    def __init__(self,config:BaseConfig) -> None:
        self.config = config

    def apt(self,libs:list,**kwargs):
        """ install distro packages using apt """
        return sp.run("sudo","apt","install",*libs,**kwargs)

    def cargo(self,libs:list,**kwargs):
        """ install rust crates using cargo """
        path = self.config.subproc['rustpath']
        return sp.run(f"{path}/cargo","install",*libs,**kwargs)
    
    def poetry(self,libs:list,**kwargs):
        """ install python packages using poetry """
        os.chdir(self.config.subproc['codepath'])
        return sp.poetry("add",*libs,**kwargs)

    def npm(self,libs:list,init=False,**kwargs):
        """ install node modules using npm """
        os.chdir(f"{self.config.root_path}/webpages")
        if init: sp.run("npm","init","--yes")
        return sp.run("npm","install",*libs,**kwargs)

    def install_libs(self,libs:dict=None,init=False):
        """ install given libs using apt,cargo,poetry,npm 
            no given libs will set init process for new project 
            and installing libs provided within config.subproc """

        if libs is None:
            init = True
            libs = self.config.subproc

        aptlibs = self.libs.get('aptlibs')
        if aptlibs: self.apt(aptlibs)

        cargolibs = self.libs.get('cargolibs')
        if cargolibs: self.cargo(cargolibs)

        pylibs = self.libs.get('pylibs')
        if pylibs: self.poetry(pylibs)

        npmlibs = self.libs.get('npmlibs')
        if npmlibs: self.npm(npmlibs,init)
