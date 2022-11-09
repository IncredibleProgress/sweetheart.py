
import os,subprocess,json,locale
from collections import UserDict
from sweetheart import MASTER_MODULE


class sp:
    """ namespace providing basic subprocess features 
        beware that it uses BaseConfig and not config """

    # convenient functions for executing bash commands
    run = lambda *args,**kwargs: subprocess.run(args,**kwargs)
    shell = lambda str,**kwargs: subprocess.run(str,**kwargs,shell=True)
    stdout = lambda str: subprocess.run(str,text=True,capture_output=True,shell=True).stdout.strip()
    
    @classmethod
    def read_sh(cls,script:str):
        """ excec line by line a long string as a shell script """
        for instruc in script.splitlines():
            cls.shell(instruc.strip())

    # let ensuring that a shell command is available
    is_executable = lambda cmd: cmd in sp.list_executables(cmd)

    BIN = (f"{os.path.expanduser('~')}/.local/bin","/usr/local/bin","/usr/bin","/bin")
    EXECUTABLES = {} # fetched by list_executables()
    MISSING = [] # fetched by list_executables()

    @classmethod
    def list_executables(cls,executables:str) -> list:
        # check executables availability
        env_ = [path for path in cls.BIN if path in os.environ["PATH"]]
        for cmd in executables.split():
            paths= [p for p in env_ if os.path.isfile(f"{p}/{cmd}")]
            version = cls.stdout(f"{cmd} --version")
            if paths: cls.EXECUTABLES.update({
                # str pattern -> "cdm::path::version"
                cmd: f"{cmd}::{paths[0]}::{version}" })
        # build the missing list
        cls.MISSING = [m for m in executables.split() if m not in cls.EXECUTABLES]
        # return list of executables
        return list(cls.EXECUTABLES)

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
        # no python env given is forbidden here
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

    @classmethod
    def set_project_env(cls,project_name:str):
        """ create and init new project with its own python env """

        assert project_name != MASTER_MODULE
        _path = f"{BaseConfig.HOME}/.sweet/{project_name}"

        # init a new python env for new project
        os.makedirs(f"{_path}/programs",exist_ok=True)
        sp.poetry("new","my_python",cwd=f"{_path}/programs")
        sp.set_python_env(cwd=f"{_path}/programs/my_python")

        os.makedirs(f"{_path}/configuration",exist_ok=True)
        with open(f"{_path}/configuration/subproc.json","w") as fi:
            json.dump({'pyenv':config.python_env},fi)


# set default configuration
class BaseConfig(UserDict):

    # stdout messages settings
    verbosity = 0
    label = MASTER_MODULE # used within echo()

    # get distrib infos on debian/ubuntu
    distrib = sp.stdout("lsb_release -is").lower()
    codename = sp.stdout("lsb_release -cs").lower()

    # get environment settings
    PWD = os.getcwd()
    HOME = os.path.expanduser('~')
    LANG = locale.getlocale()[0][0:2]
    WSL_DISTRO_NAME = os.getenv('WSL_DISTRO_NAME')

    # set sws level into environment 
    SWSLVL = os.environ['SWSLVL'] = f"{int(os.getenv('SWSLVL','0'))+1}"

    # default path settings
    poetry_bin = f"{HOME}/.local/bin/poetry"
    python_bin = "python3"# unset python env

    # default productive settings
    async_host = "http://127.0.0.1:8000"# uvicorn
    database_host = "rethinkdb://127.0.0.1:28015"
    database_admin = "http://127.0.0.1:8180"
    jupyter_host = "http://127.0.0.1:8888"
    # static_host = "http://127.0.0.1:8080"# cherrypy
    # mdbook_host = "http://127.0.0.1:3000"

    def __init__(self,project):

        # general settings
        self.project = self.label = project
        self.root_path = f"{self.HOME}/.sweet/{project}"
        self.config_file = f"{self.root_path}/configuration/config.json"
        self.subproc_file = f"{self.root_path}/configuration/subproc.json"

        # default sandbox settings
        self.is_webapp_open = True
        self.is_rethinkdb_local = True
        self.is_jupyter_local = True
        # self.is_mongodb_local = False
        # self.is_cherrypy_local = False

        # subprocess settings
        self.subproc = {
            # can be changed within set_config()
            'stsyntax': r"<% %> % {% %}",
            'rustpath': f"{self.HOME}/.cargo/bin",
            'codepath': f"{self.root_path}/programs/my_python",# no / at end
            'rethinkpath': f"{self.root_path}/database/rethinkdb",
            # 'mongopath': f"{self.root_path}/database/mongodb",
            # 'cherryconf': f"{self.root_path}/configuration/cherrypy.conf",
            
            # can not be changed within set_config()
            '.msedge.exe': f"cmd.exe /c start msedge --app=",
            '.brave.exe': f"cmd.exe /c start brave --app=",
            '.jupyterurl': f"{self.jupyter_host}/tree",
            '.jupytercmd': f"jupyterlab",
            '.tailwindcss': "npx tailwindcss -i tailwind.base.css -o tailwind.css",
        }

        # default editable settings
        self.data = {
            # editable path settings
            "working_dir": f"{self.root_path}/webpages",
            "notebooks_dir": f"{self.root_path}/documentation/notebooks",
            "templates_dir": "templates",
            "templates_base": "HTML",
            # editable subprocess settings
            "webbrowser": "default",
            "selected_db": "test",
            # editable html rendering settings
            "templates_settings": {
                # subprocess settings
                '__host__': self.async_host[7:],
                '__load__': "pylibs tailwind vue+reql",
                '__lang__': self.LANG,
                '__debug__': 1,# brython() debug argument
            },
            "static_files": {
                '/favicon.ico': "resources/favicon.ico",
                '/tailwind.css': "resources/tailwind.css",
                '/vue.js': "resources/node_modules/vue/dist/vue.global.js",
            },
            "static_dirs": {
                '/resources': f"resources",
                '/documentation': "sweetbook",
            }}


def webbrowser(url:str):
    """ start url within webbrowser set in config """

    try: select = BaseConfig._['webbrowser']
    except: select = None

    if select and '.'+select in BaseConfig._.subproc:
        sp.shell(BaseConfig._.subproc['.'+select]+url)

    elif BaseConfig._.WSL_DISTRO_NAME:
        sp.shell(BaseConfig._.subproc['.msedge.exe']+url)

    else: sp.python("-m","webbrowser",url)


_msg_ = []
def echo(*args,mode:str="default",blank:bool=False):
    """ convenient function for printing admin messages
        mode attribute must be default|stack|0|release|exit """

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
    """ convenient function for verbose messages """

    if BaseConfig.verbosity >= level:
        print(f"sws:{BaseConfig.SWSLVL}:",*args)
