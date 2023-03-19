
import subprocess
from sweetheart import *

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
        # provide system info if not
        import csv
        os_release = {}
        with open("/etc/os-release") as fi:
             reader = csv.reader(fi,delimiter="=")
             for line in reader:
                if line==[]: continue # this can happen...
                os_release[line[0]] = line[1]

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
        #FIXME: lead jupyter/jupyterlab/jupyterhub matter
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

