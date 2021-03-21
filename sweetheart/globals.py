
import os,sys
from collections import UserDict


# set default configuration
class BaseConfig(UserDict):

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
            'codepath': f"{self.root_path}/programs/my_python",# no / at the end
            'mongodb': f"mongod --dbpath={self.root_path}/database"
        }

        # default editable settings
        self.data = {

            "working_dir": f"{self.root_path}/webpages",
            "webbook": f"{self.root_path}/webpages/markdown_book/index.html",
            "webbrowser": "app:msedge.exe", # msedge.exe|brave.exe|firefox
            "terminal": "wsl",# xterm|winterm|wsl

            "templates_dir": "bottle_templates",
            "templates_settings": {

                "_default_libs_": "knacss py",
                "_async_": self.async_host,
                "_static_": "",# ""=disabled
            },
            "static_files": {"favicon": "usual_resources/favicon.ico"},
            "static_dirs": {

                "/resources": "usual_resources",
                "/libs": "javascript_libs",
                "/modules": "node_modules",
                "/documentation": "sweet_documentation",
            },
            "cherrypy": {"/":f"{self.root_path}/configuration/cherrypy.conf"},
            "db_path": f"{self.root_path}/database",
            "db_select": "demo",
        }


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
