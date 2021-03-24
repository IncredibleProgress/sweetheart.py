
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
            beware that path must exist and contain a poetry project """

        os.chdir(path)
        venv = cls.poetry("env","info","--path",
            text=True,capture_output=True).stdout.strip()

        if venv == "":
            raise Exception("Error, no python env found")

        BaseConfig.python_bin = f"{venv}/bin/python"
    

def init(config:BaseConfig):
    """ set require configuration before sweetheart installation
        and intends to provide minimalistic sweetheart features """

    # require directories
    for basedir in [
        f"{config.root_path}/configuration",
        f"{config.root_path}/database",
        f"{config.root_path}/documentation",
        f"{config.root_path}/programs/scripts",
        f"{config.root_path}/webpages/resources",
        f"{config.root_path}/webpages/markdown",
        f"{config.root_path}/webpages/{config['templates_dir']}",
    ]: os.makedirs(basedir,exist_ok=True)

    # provide default libs
    config.subproc.update({
        'pylibs': [
            "bottle",
            "pymongo",
            "uvicorn",
            "aiofiles",
            "starlette",
            "jupyterlab",
        ],
        'aptlibs': ["xterm","rustc","mongodb","npm"],
        'cargolibs': ["mdbook","mdbook-toc"],
        'npmlibs': ["brython"] })

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

    # provide OS javascript libs (Ubuntu)
    os.symlink("/usr/share/javascript",
        f"{config.root_path}/webpages/resources/javascript")


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

        os.chdir(f"{self.config.root_path}/webpages/resources")
        if init: sp.run("npm","init","--yes")
        return sp.run("npm","install",*libs,**kwargs)

    def install_libs(self,libs:dict=None,init=False):
        """ install given libs using apt,cargo,poetry,npm 
            no given libs will set init process for new project 
            and install libs provided within config.subproc """

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


class BaseService:

    wsl = lambda cmd: f"cmd.exe /c start wsl {cmd} &"
    winterm = lambda cmd: f"cmd.exe /c start wt wsl {cmd} &"
    xterm = lambda cmd: f"xterm -C -geometry 190x19 -e {cmd} &"

    def __init__(self,url:str,config:BaseConfig) -> None:
        """ set basic features of sweeheart service objects
            given url should follow http://host:port pattern
            the child class must set the command attribute """

        self.config = config
        self.command = "echo Error, no command attribute given"

        if config.WSL_DISTRO_NAME: self.terminal = 'wsl'
        else: config.terminal = 'xterm'

        self.url = url
        self.host = url.split(":")[1].strip("/")
        self.port = int(url.split(":")[2])

    def run_local(self,service:bool=True):
        """ start and run the command attribute locally
            self.command must be set previously """

        if service:
            assert self.terminal in "xterm|winterm|wsl"
            # run service locally opening new shell
            sp.shell(getattr(self,self.terminal)(self.command),
                stderr=subprocess.DEVNULL)
        else:
            # run service locally within current shell
            sp.shell(self.command)
            
    def run_server(self):
        raise NotImplementedError

    def cli_func(self,args):
        """ given function for command line interface """
        raise NotImplementedError
