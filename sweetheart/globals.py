
import os,sys
from collections import UserDict


# set default configuration
class BaseConfig(UserDict):

    # set messages to stdout
    verbosity = 0
    label = "sweetheart"

    # get environment settings
    USER = os.environ['USER']
    HOME = os.environ['HOME']
    PWD = os.environ['PWD']
    WSL_DISTRO_NAME = os.getenv('WSL_DISTRO_NAME')

    # default paths settings
    poetry_bin = f"{HOME}/.poetry/bin/poetry"
    python_bin = "python3"# venv disabled

    def __init__(self,project) -> None:

        # general settings
        self.project = self.label = project
        self.root_path = f"{self.HOME}/.sweet/{project}"
        self.config_file = f"{self.root_path}/configuration/sweet.json"

        # default sandbox settings
        self.is_webapp = True
        self.is_mongodb_local = True
        self.is_uvicorn_local = True
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
            'msedge.exe': f"cmd.exe /c start msedge --app={self.async_host}",
            'firefox': f"firefox {self.async_host}",
        }

        # default editable settings
        self.data = {

            "working_dir": f"{self.root_path}/webpages",
            "db_select": "demo",

            "templates_dir": "templates",
            "templates_settings": {
                "_default_libs_": "knacss py",
                "_async_": self.async_host,
                "_static_": "",# ""=disabled
            },
            "static_files": {
                "/favicon.ico": "resources/favicon.ico",
            },
            "static_dirs": {
                "/resources": "resources",
            },
            "cherrypy": {
                "/": f"{self.root_path}/configuration/cherrypy.conf",
            },
        }

        # set a default html welcome message
        self.welcome = f"""
          <div style="text-align:center;">
            <h1><br><br>Welcome {self.USER.capitalize()} !<br><br></h1>
            <h3>sweetheart</h3>
            <p>a supercharged heart for the non-expert hands</p>
            <p>that will give you full power at the speedlight</p>
            <p><a href="documentation/index.html"
                class="btn" role="button">Get Started Now!</a></p>
            <p><br>or code immediately using <a href="jupyter">JupyterLab</a></p>
            <p><br><br><em>this message appears because there
                was nothing else to render here</em></p>
          </div>
            """


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
