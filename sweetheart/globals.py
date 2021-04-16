
import os,subprocess,json
from collections import UserDict

# default project name 
SWEETHEART = "sweetheart"


class sp:
    """ namespace providing basic subprocess features 
        beware that it uses BaseConfig and not config """

    run = lambda *args,**kwargs: subprocess.run(args,**kwargs)
    shell = lambda str,**kwargs: subprocess.run(str,**kwargs,shell=True)

    @classmethod
    def terminal(cls,cmd:str,select:str,**kwargs):
        """ run cmd within selected terminal 
            select must be in xterm|winterm|wsl """

        wsl = f"cmd.exe /c start wsl {cmd} &"
        winterm = f"cmd.exe /c start wt wsl {cmd} &"
        xterm = f"xterm -C -geometry 190x19 -e {cmd} &"

        assert select in "xterm|winterm|wsl"
        cls.shell(eval(select),**kwargs)
        
    @classmethod
    def poetry(cls,*args,**kwargs):

        if not kwargs.get('cwd') and hasattr(BaseConfig,'_'):
            kwargs['cwd'] = BaseConfig._.subproc['codepath']

        return cls.run(BaseConfig.poetry_bin,*args,**kwargs)

    @classmethod
    def python(cls,*args,**kwargs):
        #NOTE: no python env forbidden here
        assert hasattr(BaseConfig,'python_env')
        return cls.run(BaseConfig.python_bin,*args,**kwargs)

    @classmethod
    def set_python_env(cls,**kwargs):
        """ get python venv path from poetry and set it within config
            beware that Baseconfig._ or cwd kwargs has to be given 
            when current working dir doesn't include a poetry project """

        env = cls.poetry("env","info","--path",
            text=True,capture_output=True,**kwargs).stdout.strip()
        if env == "": raise Exception("Error, no python env found")

        BaseConfig.python_env = env
        BaseConfig.python_bin = f"{env}/bin/python"
        verbose("set python env:",BaseConfig.python_bin)


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
    # set sws level into environment 
    SWSLVL = os.environ['SWSLVL'] =\
        f"{int(os.getenv('SWSLVL','0'))+1}"

    # default path settings
    poetry_bin = f"{HOME}/.poetry/bin/poetry"
    python_bin = "python3"# unknown python env

    def __init__(self,project):

        # general settings
        self.project = self.label = project
        self.root_path = f"{self.HOME}/.sweet/{project}"
        self.config_file = f"{self.root_path}/configuration/config.json"
        self.subproc_file = f"{self.root_path}/configuration/subproc.json"

        # default sandbox settings
        self.is_webapp_open = True
        self.is_mongodb_local = True
        self.is_jupyter_local = False
        self.is_cherrypy_local = False

        # default productive settings
        self.async_host = "http://127.0.0.1:8000"# uvicorn
        self.static_host = "http://127.0.0.1:8080"# cherrypy
        self.database_host = "mongodb://127.0.0.1:27017"
        self.jupyter_host = "http://127.0.0.1:8888"
        self.mdbook_host = "http://127.0.0.1:3000"

        # subprocess settings
        self.subproc = {
            'rustpath': f"{self.HOME}/.cargo/bin",
            'codepath': f"{self.root_path}/programs/my_python",# no / at end
            'mongopath': f"{self.root_path}/database",
            'cherrypy': f"{self.root_path}/configuration/cherrypy.conf",
            'msedge.exe': f"cmd.exe /c start msedge --app=",
            'brave.exe': f"cmd.exe /c start brave --app=",
            #'firefox': f"firefox ",# space is needed
        }

        # default editable settings
        self.data = {
            "working_dir": f"{self.root_path}/webpages",
            "notebooks_dir": f"{self.root_path}/documentation/notebooks",
            "selected_DB": "test",
            "webbrowser": "default",
            
            "templates_dir": "templates",
            "templates_settings": {
                "__load__": "pylibs",
                #"__async__": self.async_host,
                #"__static__": "",# ""=disabled
            },
            "static_files": {
                "/favicon.ico": "resources/favicon.ico",
            },
            "static_dirs": {
                "/resources": f"resources",
                "/documentation": "sweetbook",
            },}

    def welcome(self) -> str:
        """ return default Html welcome message """

        return f"""
          <div style="text-align:center;font-size:1.1em;">
            <h1><br><br>Welcome {self.USER} !<br><br></h1>
            <h2>sweetheart</h2>
            <p>a supercharged heart for the non-expert hands</p>
            <p>which will give you coding full power at the speedlight</p>
            <p><a href="/documentation/index.html">
                Get Started Now!</a></p>
            <p><br>or code immediately using 
                <a href="{self.jupyter_host}">JupyterLab</a></p>
            <p><br><br><em>this message appears because there
            was nothing else to render here</em></p>
          </div>"""


# provide convenient functions for givin messages
_msg_ = []
def echo(*args,mode="default",blank=False):
    """convenient function for printing messages
    mode = 0|default|stack|release"""

    if blank: print()
    
    if mode.lower() == "stack" or mode == 0:
        global _msg_
        _msg_.append(" ".join(args))

    elif mode.lower() == "release":
        for msg in _msg_:
            print("[%s]"% BaseConfig.label.upper(),msg)
        _msg_ = []

    elif mode.lower() == "exit":
        print("[%s]"% BaseConfig.label.upper(),*args)
        exit()

    else:
        print("[%s]"% BaseConfig.label.upper(),*args)

def verbose(*args,level:int=1):
    """convenient function for verbose messages"""
    if BaseConfig.verbosity >= level:
        print(f"sws:{BaseConfig.SWSLVL}:",*args)
