
import os,sys,subprocess
from collections import UserDict


class sp:
    """ namespace providing basic subprocess features """

    run = lambda *args,**kwargs: subprocess.run(args,**kwargs)
    shell = lambda str,**kwargs: subprocess.run(str,**kwargs,shell=True)

    @classmethod
    def terminal(cls,cmd:str,select:str):
        """ run cmd within selected terminal 
            select must be in xterm|winterm|wsl """

        wsl = f"cmd.exe /c start wsl {cmd} &"
        winterm = f"cmd.exe /c start wt wsl {cmd} &"
        xterm = f"xterm -C -geometry 190x19 -e {cmd} &"

        assert select in "xterm|winterm|wsl"
        cls.shell(eval(select))
        
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

        if venv == "": raise Exception("Error, no python env found")
        BaseConfig.python_bin = f"{venv}/bin/python"
        verbose("set python env:",BaseConfig.python_bin)

    @classmethod
    def exit(cls): sys.exit()


# set default configuration
class BaseConfig(UserDict):

    # set messages to stdout
    verbosity = 0
    label = "sweetheart"

    # get environment settings
    PWD = os.environ['PWD']
    HOME = os.environ['HOME']
    USER = os.environ['USER'].capitalize()
    WSL_DISTRO_NAME = os.getenv('WSL_DISTRO_NAME')

    # default paths settings
    poetry_bin = f"{HOME}/.poetry/bin/poetry"
    python_bin = None# unknown venv

    def ensure_python(self):
        """ this allows setting python_bin only when needed 
            it avoids waiting time due to poetry loading """

        if self.python_bin is None:
            sp.set_python_env(path=self.subproc['codepath'])

    def __init__(self,project) -> None:

        # general settings
        self.project = self.label = project
        self.root_path = f"{self.HOME}/.sweet/{project}"
        self.config_file = f"{self.root_path}/configuration/sweet.json"

        # default sandbox settings
        self.is_webapp = True
        self.is_mongodb_local = True
        self.is_jupyter_local = False
        self.is_cherrypy_local = False

        # default productive settings
        self.async_host = "http://localhost:8000"# uvicorn
        self.static_host = "http://localhost:8080"# cherrypy
        self.database_host = "mongodb://localhost:27017"# mongoDB
        self.jupyter_host = "http://localhost:8888"# jupyterlab

        # subprocess settings
        self.subproc = {
            'rustpath': f"{self.HOME}/.cargo/bin",
            'codepath': f"{self.root_path}/programs/my_python",# no / at end
            'mongodb': f"mongod --dbpath={self.root_path}/database",
            'msedge.exe': f"cmd.exe /c start msedge --app=",
            'firefox': f"firefox ",# space is needed
        }

        # default editable settings
        self.data = {
            "working_dir": f"{self.root_path}/webpages",
            "db_select": "demo",

            "templates_dir": "templates",
            "templates_settings": {
                "_default_libs_": "py",
                "_async_": self.async_host,
                "_static_": "",# ""=disabled
            },
            "static_files": {
                #"/favicon.ico": "resources/favicon.ico",
            },
            "static_dirs": {
                "/resources": "resources",
            },
            "cherrypy": {
                "/": f"{self.root_path}/configuration/cherrypy.conf",
            },}


# set a default html welcome message
WELCOME = f"""
  <div style="text-align:center;font-size:1.2em;">
    <h1><br><br>Welcome {BaseConfig.USER} !<br><br></h1>
    <h3>sweetheart</h3>
    <p>a supercharged heart for the non-expert hands</p>
    <p>that will give you full power at the speedlight</p>
    <p><a href="documentation/index.html">Get Started Now!</a></p>
    <p><br>or code immediately using <a href="jupyter">JupyterLab</a></p>
    <p><br><br><em>this message appears because there
      was nothing else to render here</em></p>
  </div>"""


# provide convenient functions for givin messages
_msg_ = []
def echo(*args,mode="default"):
    """convenient function for printing messages
    mode = 0|default|stack|release"""

    if mode.lower() == "stack" or mode == 0:
        global _msg_
        _msg_.append(" ".join(args))

    elif mode.lower() == "release":
        for msg in _msg_:
            print("[%s]"% BaseConfig.label.upper(),msg)
        _msg_ = []

    elif mode.lower() == "exit":
        print("[%s]"% BaseConfig.label.upper(),*args)
        sys.exit()

    else:
        print("[%s]"% BaseConfig.label.upper(),*args)

def verbose(*args,level:int=1):
    """convenient function for verbose messages"""
    if BaseConfig.verbosity >= level: print(*args)
