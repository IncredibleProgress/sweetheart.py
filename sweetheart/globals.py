
import os,subprocess,json,locale
from collections import UserDict

# default dir/module name of master project
#FIXME: allow replacing sweetheart by a fork of it
MASTER_MODULE = "sweetheart"


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


# set default configuration
class BaseConfig(UserDict):

    # set messages to stdout
    verbosity = 0
    label = "sweetheart"# used for print with echo()
    locale_lang = locale.getlocale()[0][0:2]

    # get environment settings
    PWD = os.environ['PWD']
    HOME = os.environ['HOME']
    USER = os.environ['USER'].capitalize()
    WSL_DISTRO_NAME = os.getenv('WSL_DISTRO_NAME')
    # set sws level into environment 
    SWSLVL = os.environ['SWSLVL'] = f"{int(os.getenv('SWSLVL','0'))+1}"

    # default path settings
    poetry_bin = f"{HOME}/.local/bin/poetry"
    python_bin = "python3"# unset python env

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

        # default productive settings
        #FIXME: port matter should be improved in BaseService
        self.async_host = "http://127.0.0.1:8000"# uvicorn
        self.database_host = "rethinkdb://127.0.0.1:28015"
        self.database_admin = "http://127.0.0.1:8180"
        self.jupyter_host = "http://127.0.0.1:8888"
        # self.static_host = "http://127.0.0.1:8080"# cherrypy
        # self.mdbook_host = "http://127.0.0.1:3000"

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
            "selected_DB": "test",
            # editable html rendering settings
            "templates_settings": {
                # subprocess settings
                '__host__': self.async_host[7:],
                '__load__': "tailwind pylibs vue+reql",
                '__lang__': self.locale_lang,
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

    def welcome(self) -> str:
        """ return default Html welcome message """

        if self.is_jupyter_local:
            # enable html link to running Jypyter local server
            jupyter_link = f"""<p><br>or code immediately using 
                <a href="{self.subproc['.jupyterurl']}">JupyterLab</a></p>"""
        else: jupyter_link = ""

        return f"""
          <div style="text-align:center;font-size:1.1em;">
            <h1><br><br>Welcome {self.USER} !<br><br></h1>
            <h2>sweetheart</h2>
            <p>a supercharged heart for the non-expert hands</p>
            <p>which will give you coding full power at the light speed</p>
            <p><a href="/documentation/index.html">
                Get Started Now!</a></p>
            {jupyter_link}
            <p><br><br><em>this message appears because there
            was nothing else to render here</em></p>
          </div>"""


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
