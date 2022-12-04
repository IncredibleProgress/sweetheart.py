
import os,subprocess,json,locale
from collections import UserDict
from sweetheart import MASTER_MODULE


class BaseConfig(UserDict):
    """ configuration settings base class

        use the get_config() func for getting a new instance 
        BaseConfig._ return the last config created with it """

    # stdout messages settings
    verbosity = 0
    label = MASTER_MODULE # used within echo()

    # get environment settings
    PWD = os.getcwd()
    HOME = os.path.expanduser('~')
    USER = HOME.split('/')[-1]
    LANG = locale.getlocale()[0][0:2]
    WSL_DISTRO_NAME = os.getenv('WSL_DISTRO_NAME')

    # set sws level into environment 
    SWSLVL = os.environ['SWSLVL'] = f"{int(os.getenv('SWSLVL','0'))+1}"
    assert int(SWSLVL) <= 2

    # default path settings
    poetry_bin = f"{HOME}/.local/bin/poetry"
    python_bin = "python3"# here python env is unset
    rust_crates = f"{HOME}/.cargo/bin"

    # default productive settings
    async_host = "http://127.0.0.1:8000"# uvicorn
    database_host = "rethinkdb://127.0.0.1:28015"
    database_admin = "http://127.0.0.1:8180"
    jupyter_host = "http://127.0.0.1:8888"

    def __init__(self,project):

        # general settings
        self.project = self.label = project
        self.root_path = f"{self.HOME}/.sweet/{project}"
        self.config_file = f"{self.root_path}/configuration/config.json"
        self.subproc_file = f"{self.root_path}/configuration/subproc.json"

        # default services settings
        self.is_webapp_open = True
        self.is_rethinkdb_local = True
        self.is_jupyter_local = True
        self.is_nginx_local = True

        # subprocess settings
        self.subproc = {
            #  can be updated using load_json(subproc=True)
            'python_version': "3.10",# for setting Nginx Unit
            'node_version': "16.x",# for getting node from nodesource.com
            # can not be updated within load_json(subproc=True)
            '.msedge.exe': f"cmd.exe /c start msedge --app=",
            '.brave.exe': f"cmd.exe /c start brave --app=",
            '.tailwindcss': "npx tailwindcss -i tailwind.base.css -o tailwind.css" }

        self.data = {
            # editable general settings
            "db_name": "test",
            "templates_base": "HTML",
            "templates_dir": "templates",
            "stsyntax": r"<% %> % {% %}",
            "working_dir": f"{self.root_path}/webpages",
            "db_path": f"{self.root_path}/database/rethinkdb",
            "module_path": f"{self.root_path}/programs/my_python",# no / at end

            # editable services settings
            #FIXME: multi-databases support to implement
            "webbrowser": "default",
            "jupyter_url": f"{self.jupyter_host}/tree",
            "notebooks_dir": f"{self.root_path}/documentation/notebooks",

            # editable html rendering settings
            "templates_settings": {
                '__lang__': self.LANG,
                '__host__': self.async_host[7:],
                '__load__': "pylibs tailwind vue+reql",
                '__debug__': 1,# brython() debug argument
            },
            "static_files": {
                '/favicon.ico': "resources/favicon.ico",
                '/tailwind.css': "resources/tailwind.css",
                '/vue.js': "resources/node_modules/vue/dist/vue.global.js",
            },
            "static_dirs": {
                '/resources': f"resources",
                #'/documentation': "sweetbook",
            }}

    def __getattr__(self,attr):
        """ search non-existing attribute into self.data and self.subproc
            config.db_name cab be used instead of config['db_name'] """
        
        #! order: 1=obj.attr 2=subproc 3=data
        try: return self.subproc[attr]
        except: return self.data[attr]

    def load_json(self,subproc=False):
        """ update config from given json file """

        if os.path.isfile(self.config_file):

            with open(self.config_file) as file_in:
                config.update(json.load(file_in))
                verbose("config file:",self.config_file)

        if not subproc: return
        elif os.path.isfile(self.subproc_file):
            # update self.subproc for allowed keys

            with open(self.subproc_file) as file_in:
                subproc_settings = json.load(file_in)
                verbose("subproc file:",self.subproc_file)

            for key,value in subproc_settings.items():

                if key.startswith('.'): 
                    echo(f"WARNING: update of subproc setting '{key}' forbidden")
                    continue
                if key == 'pyenv': 
                    BaseConfig.python_env = value
                    BaseConfig.python_bin = f"{value}/bin/python"
                else:
                    self.subproc[key] = value


class sp:
    """ namespace providing basic subprocess features 
        beware that it uses BaseConfig and not config """

    PATH = os.get_exec_path()
    EXECUTABLES = {} # fetched by list_executables()
    MISSING = [] # fetched by list_executables()

    try:
        # provide system info for Python3.10 and more
        from platform import freedesktop_os_release
        os_release = freedesktop_os_release()
    except:
        #FIXME: provide system info up to Python 3.9
        raise NotImplementedError("Python version <= 3.9")

    @classmethod
    def shell(cls,*args,**kwargs):
        """ run subprocess providing some flexibility with args """

        if len(args)==1 and isinstance(args[0],str):
            # string passed to the linux shell
            kwargs.update({ 'shell':True })
            return subprocess.run(args[0],**kwargs)

        elif len(args)==1 and isinstance(args[0],list) and\
                all([ isinstance(i,str) for i in args[0] ]):
            # list of strings passed to the linux shell
            return subprocess.run(args[0],**kwargs)
        
        elif all([ isinstance(i,str) for i in args ]):
            # str args passed to the linux shell
            return subprocess.run(args,**kwargs)

        else: raise AttributeError

    @classmethod
    def read_sh(cls,script:str):
        """ excec line by line a long string as a shell script """

        for instruc in script.splitlines():
            subprocess.run(instruc.strip(),shell=True)

    # former provided function for executing shell commands
    run = lambda *args,**kwargs: subprocess.run(args,**kwargs)

    # provide a direct way for getting the stdout
    stdout = lambda *args,**kwargs:\
        sp.shell(*args,text=True,capture_output=True,**kwargs).stdout.strip()

    # let ensuring that a shell command is available
    is_executable = lambda cmd: cmd in sp.list_executables(cmd)

    @classmethod
    def list_executables(cls,executables:str) -> list:

        # check executables availability
        for cmd in executables.split():
            try:
                # will fail if cmd is not executable
                version = cls.stdout(f"{cmd} --version")

                # search the first executable path
                for pth in cls.PATH:
                    if os.path.isfile(f"{pth}/{cmd}"):
                        cls.EXECUTABLES.update({
                            # str pattern -> "cdm::path::version"
                            cmd: f"{pth} :: {version}" })
                        break
            except:
                continue

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
            kwargs['cwd'] = BaseConfig._['module_path']

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
    def init_project_env(cls,project_name:str):
        """ create and init new project with its own python env """

        assert project_name != MASTER_MODULE
        _path = f"{BaseConfig.HOME}/.sweet/{project_name}"

        # init a new python env for new project
        os.makedirs(f"{_path}/documentation/notebooks",exist_ok=True)
        os.makedirs(f"{_path}/configuration",exist_ok=True)
        os.makedirs(f"{_path}/programs",exist_ok=True)

        sp.poetry("new","my_python",cwd=f"{_path}/programs")
        sp.poetry("add",MASTER_MODULE,cwd=f"{_path}/programs/my_python")
        sp.set_python_env(cwd=f"{_path}/programs/my_python")

        with open(f"{_path}/configuration/subproc.json","w") as fi:
            json.dump({ 'pyenv': BaseConfig.python_env },fi)

        # manage the specific case of jupyter
        if project_name.startswith("jupyter"):

            from sweetheart.sweet import set_config
            from sweetheart.heart import JupyterLab

            config = set_config(project="jupyter")
            sp.poetry("add",project_name)
            JupyterLab(config).set_ipykernel(pwd=True)


def webbrowser(url:str):
    """ start url within a webbrowser set in config 
        it leads running on the WSL with Windows 10/11 """

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
