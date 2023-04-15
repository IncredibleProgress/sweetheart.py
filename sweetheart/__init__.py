"""
SWEETHEART 0.1.x 'new age rising'
Rock-solid pillars for innovative and enterprise-grade apps.

*Start from scratch and create with ease and efficiency the apps you really need
embedding reliable open-source code, highest quality components, best practices.*

About __init__.py :

    imports python modules: sys, json
    provides: set_config, quickstart, HTMLTemplate
    the python os module is replaced by an os class
    (non-exhaustive)

 Sweetheart 0.1.x includes an adapted version of bottle.py,
 which is not a part of the sweetheart project itself. Info:

    Homepage and documentation: http://bottlepy.org/
    Copyright (c) 2016, Marcel Hellkamp.
    License: MIT (see LICENSE for details)
"""

import sys,json
from collections import UserDict
from sweetheart.subprocess import os

__version__ = "0.1.2"
__license__ = "CeCILL-C FREE SOFTWARE LICENSE AGREEMENT"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"

# default dir/module name of master project
#FIXME: allow replacing sweetheart by a fork of it
MASTER_MODULE = "sweetheart"


class BaseConfig(UserDict):
    """ configuration settings base class

        use the get_config() func for getting a new instance 
        BaseConfig._ return the last config created with it """

    # stdout messages settings
    logg = []
    verbosity = 0
    label = MASTER_MODULE # printed with echo()

    # get environment settings
    HOME = os.path.expanduser('~')
    WSL_DISTRO_NAME = os.getenv('WSL_DISTRO_NAME')

    # default path settings
    python_bin = sys.executable
    poetry_bin = f"{HOME}/.local/bin/poetry"
    rust_crates = f"{HOME}/.cargo/bin"

    def __init__(self,project):

        # general settings
        self.run = '__undefined__'
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
            # default local servers settings
            # can be updated using load_json(subproc=True)
            "async_host": "http://127.0.0.1:8000",
            "database_host": "RethinkDB://127.0.0.1:28015",
            "database_admin": "http://127.0.0.1:8180",
            "jupyter_host": "http://127.0.0.1:8888",
            "nginxunit_host": "http://localhost",

            # default low level settings
            # can be updated using load_json(subproc=True)
            'systemd': [],
            'unit_listener': "*:80",
            'python_version': "3.10",# used for setting Nginx Unit
            'node_version': "16.x",# used getting node from nodesource.com
            'stsyntax': r"<% %> % {% %}",

            # can not be updated within load_json(subproc=True)
            # the settings are locked because key starts with .
            '.msedge.exe': f"cmd.exe /c start msedge --app=",
            '.brave.exe': f"cmd.exe /c start brave --app=",
            '.tailwindcss': "npx tailwindcss -i tailwind.base.css -o tailwind.css" }

        self.data = {
            # editable general settings
            "db_name": "test",
            "app_module": "start",#! no .py suffix here
            "app_callable": "webapp",
            "templates_base": "HTML",
            "templates_dir": "templates",
            
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
                #'__lang__': self.LANG,
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
                #'/documentation': "sweetdoc",
                #FIXME: documentation to integrate better
            }}

    def __getattr__(self,attr):
        """ search non-existing attribute into self.subproc and self.data
            example: config.db_name can be used instead of config['db_name'] """
        
        # search order: 1=obj.attr 2=subproc 3=data
        # it means subproc has priority over data 
        try: return self.subproc[attr]
        except: return self.data[attr]

    def __enter__(self):
        """
        this allows context management with configs using set_config()
        it should avoid misconfigurations when using more than 1 config

            with set_config(project="jupyter") as cfg:
                JupyterLab(cfg).run_local(terminal='wsl')
        """
        BaseConfig.__conf = BaseConfig._
        return self

    def __exit__(self,exc_type,exc_value,exc_tb):

        BaseConfig._ = BaseConfig.__conf
        del BaseConfig.__conf
        
    def load_json(self,subproc:bool=False):
        """ update config object from given json file """

        if os.path.isfile(self.config_file):

            with open(self.config_file) as file_in:
                self.update(json.load(file_in))
                verbose("load config file:",self.config_file)

        if not subproc:
            return

        elif os.path.isfile(self.subproc_file):
            
            # update self.subproc for allowed keys
            with open(self.subproc_file) as file_in:
                subproc_settings = json.load(file_in)
                verbose("load subproc file:",self.subproc_file)

            for key,value in subproc_settings.items():

                if key.startswith('.'): 
                    echo(f"WARNING: update subproc setting '{key}' forbidden")
                    continue
                if key == 'pyenv': 
                    self.python_env = value
                    self.python_bin = f"{value}/bin/python"
                else:
                    self.subproc[key] = value


def set_config(
    values:dict = {},
    project:str = MASTER_MODULE,
    config_file:str = None ) -> BaseConfig :

    """ set or reset sweetheart configuration with ease
        allow working with different projects and configs 
        BaseConfig._ provides a hook to the last set config """

    # allow setting project within dict values
    if isinstance(values,dict) and values.get('project'):
        project = values['project']
        del values['project']#! avoid confusion

    # BaseConfig._ is the last set config
    config = BaseConfig._ = BaseConfig(project)

    if config_file:
        config.config_file = config_file

    elif isinstance(values,str):
        # allow catching config_file instead of values
        if os.path.isfile(values) and values[:-5]==".json":
            config.config_file = config_file = values

    # update config from json conf file
    try: config.load_json(subproc=True)
    except: echo("WARNING: json config files loading failed")

    if "init" not in sys.argv :
        # ensure python env setting when not given by subproc_file
        try: config.python_env
        except: sp.set_python_env()
        verbose("python env:",config.python_env)

    # provide shortcut for setting running env
    if values.get('run'):

        config.run = values['run']
        assert config.run in "testing|productive"
        del values['run']#! avoid confusion

        if config.run == "productive":

            config.is_webapp_open = False
            config.is_rethinkdb_local = False
            config.is_jupyter_local = False

            echo("INFO: running for production")
            BaseConfig.untrusted_code_forbidden = True

    # update config and return
    config.update(values)
    return config


def quickstart(*args,_cli_args=None):

    """ build and run webapp for the current config (autoset when not given)
        usually args should be a HttpServer instance or Route|Mount objects
        however for tests it can be a template or even Html code directly
        NOTE: this flexibility is provided by mount() method of HttpServer """

    # extra imports
    from sweetheart.services import \
        RethinkDB,JupyterLab,HttpServer

    # allow auto config if missing
    try: config = BaseConfig._
    except: config = set_config()

    if _cli_args:
        # update current config from cli
        config.is_webapp_open = not _cli_args.server_only
        config.is_rethinkdb_local = not _cli_args.db_disabled
        config.is_jupyter_local = _cli_args.jupyter_lab
    
    if config.is_jupyter_local:
        # set and run Jupyterlab server
        _path = "/etc/systemd/system/jupyterlab.service"
        if os.isfile(_path): kwargs= {'service':'jupyterlab'}
        else: kwargs= {'terminal':True}

        with set_config(project="jupyter") as cfg:
            JupyterLab(cfg).run_local(**kwargs)

    if args and isinstance(args[0],HttpServer):
        # set webapp from a given HttpServer instance
        webapp = args[0]
    else:
        # build new webapp from Route|Mount objects,html code or template
        webapp = HttpServer(config,set_database=config.is_rethinkdb_local)
        webapp.mount(*args)
        
        # if config.is_rethinkdb_local:
        #     # set and run RethinkDB server
        #     webapp.database = RethinkDB(config,run_local=True)
        #     webapp.database.set_websocket()
        #     webapp.database.set_client()
        
    # start webapp within current bash
    webapp.run_local(service=None)


  #############################################################################
 ## HTML handling ############################################################
#############################################################################

def HTMLTemplate(filename:str,**kwargs):
    """ provide a Starlette-like function for rendering templates
        including configuration data and some python magic stuff """

    # extra imports
    from sweetheart.bottle import SimpleTemplate
    from starlette.responses import HTMLResponse

    # set templates dir as working dir
    os.chdir(BaseConfig._.working_dir)

    if os.path.isfile(f"{BaseConfig._.templates_dir}/{filename}"):
        # load template from filename if exists
        with open(f"{BaseConfig._.templates_dir}/{filename}","r") as tpl:
            template = tpl.read()

    elif isinstance(filename,str):
        # alternatively test the given string as template
        template = filename

    else: raise Exception

    for old,new in {
      # provide magic html rebase() syntax <!SWEETHEART html>
      f'<!{MASTER_MODULE.upper()} html>': \
          f'%rebase("{BaseConfig._.templates_base}")',

      # provide magic html facilities
      ' s-style>': ' class="sw">',
      ' s-style="': ' class="sw ', # switch for tailwindcss
      '<vue': '<div v-cloak id="VueApp"',
      '</vue>': '</div>',

      # provide magic <python></python> syntax
      '</python>': "</script>",
      '<python>': """<script type="text/python">
import json
from browser import window, document
console, r = window.console, window.r
def try_exec(code:str):
    try: exec(code)
    except: pass
def createVueApp(dict):
    try_exec("r.onupdate = on_update")
    try_exec("r.onmessage = on_message")
    try_exec("window.vuecreated = vue_created")
    window.createVueApp(json.dumps(dict))\n""",

      }.items():
        template = template.replace(old,new)
    
    # render html from template and config
    template = SimpleTemplate(template)
    return HTMLResponse(template.render(
        __db__ = BaseConfig._.db_name,
        **BaseConfig._.templates_settings,
        **kwargs ))


def build_css():
    """ build or rebuild tailwind.css file """
    
    sp.shell(BaseConfig._.subproc['.tailwindcss'],
        cwd=f"{BaseConfig._.root_path}/webpages/resources")


def test_template(template:str):

    from sweetheart.services import HttpServer,Route

    BaseConfig.verbosity = 1
    assert hasattr(BaseConfig,'_')
    
    BaseConfig._.is_webapp_open = True
    BaseConfig._.is_rethinkdb_local = False
    BaseConfig._.is_jupyter_local = False

    path = f"{BaseConfig._.working_dir}/{BaseConfig._.templates_dir}"
    if not os.path.isfile(path) and not os.path.islink(path):
        echo("Error, the given template is not existing")
        exit()

    webapp = HttpServer(BaseConfig._,set_database=False).mount(
        Route("/",HTMLTemplate(template)) )

    quickstart(webapp)


def webbrowser(url:str):
    """ start url within the webbrowser set in config 
        it allow running on the WSL with Windows 10/11 """

    try: select = BaseConfig._.webbrowser
    except: select = None

    if select and '.'+select in BaseConfig._.subproc:
        sp.shell(BaseConfig._.subproc['.'+select]+url)

    elif BaseConfig._.WSL_DISTRO_NAME:
        sp.shell(BaseConfig._.subproc['.msedge.exe']+url)

    else: sp.python("-m","webbrowser",url)


  #############################################################################
 ## Subprocesses handling ####################################################
#############################################################################

class sp(os):
    """
    namespace providing basic subprocess features 
    beware that it uses BaseConfig and not config 
        
    >>> sp.stdout("which python3")
    >>> sp.is_executable("cargo")
    """

    # provide a direct way for getting the shell stdout 
    stdout = lambda *args,**kwargs:\
        sp.shell(*args,text=True,capture_output=True,**kwargs).stdout.strip()

    @classmethod
    def shell(cls,*args,**kwargs):
        """ run bash command providing some flexibility with args """

        if len(args)==1 and isinstance(args[0],str):
            kwargs.update({ 'shell':True })
            return cls.run(args[0],**kwargs)

        elif len(args)==1 and isinstance(args[0],list):
            return cls.run(args[0],**kwargs)
        
        else: 
            # zip the args into a list given as first arg to run()
            # allow shell("echo","hello") rather than shell(["echo","hello"])
            return cls.run(args,**kwargs)

    @classmethod
    def read_sh(cls,script:str):
        """ excec line by line a long string as a shell script """

        for instruc in script.splitlines():
            cls.run(instruc.strip(),shell=True)

    @classmethod
    def sudo(sp,*args,**kwargs):
        """ a Jupyter compliant sudo cmd that runs sudo -S
            this will ask sudo password at the first call """

        command = ' '.join(args)
        assert getattr(sp,'_ALLOW_SUDO_','NO') == '__YES__'

        if getattr(sp,'_getpass_',False) is True: 
            # don't ask for sudo password here
            return sp.shell(f"sudo -S {command}",**kwargs)

        else: # ask for sudo password and avoid echo of it
            sudopass= lambda passwd: f"echo {passwd} | sudo -S {command}"
            askpass= lambda: os.getpass("sudo passwd required: ")

            process= sp.shell(sudopass(askpass()),**kwargs)
            process.args= sudopass("****")

            sp._getpass_ = True
            return process

    @classmethod
    def systemctl(cls,*args,**kwargs):

        """ exec the systemctl shell cmd with sudo and
            doesn't require allowing sudo previously 
            this is made for executing a single shot
            don't use it within @sudo decorated func """

        # try: run = BaseConfig._.run
        # except: run = '__undefined__'

        # assert run != '__undefined__'
        cls._ALLOW_SUDO_ = '__YES__'
        cls.sudo("systemctl",*args,**kwargs)
        del cls._ALLOW_SUDO_

    @classmethod
    def overwrite_file(cls,content:str,file:str,cwd:str=None):
        
        if cwd: os.chdir(cwd)
        with open(file,'w') as file_out:
            file_out.write(content.strip())


    EXECUTABLES = {} # fetched by list_executables()
    MISSING = [] # fetched by list_executables()

    @classmethod
    def list_executables(cls,executables:str) -> list:

        exe = executables.split()
        pth = [ os.which(cmd) for cmd in exe ]

        for index in range(len(exe)):
            if pth[index] is not None:
                cls.EXECUTABLES.update(
                    { exe[index]: pth[index] })
                        
        cls.MISSING = [m for m in exe if m not in cls.EXECUTABLES]
        return list(cls.EXECUTABLES)

    # let ensuring that a shell command is available
    is_executable = lambda cmd:\
        cmd in sp.list_executables(cmd)


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

        try: poetbin = BaseConfig._.poetry_bin
        except: poetbin = BaseConfig.poetry_bin

        return cls.shell(poetbin,*args,**kwargs)

    @classmethod
    def python(cls,*args,**kwargs):

        try:
            _conf_ = BaseConfig._
            pythbin = BaseConfig._.python_bin
        except:
            verbose("WARN: python bin provided by BaseConfig")
            # run sp.python() without provided config
            _conf_ = BaseConfig
            pythbin = BaseConfig.python_bin

        # no env is forbidden here
        assert hasattr(_conf_,"python_env")

        return cls.shell(pythbin,*args,**kwargs)

    @classmethod
    def set_python_env(cls,**kwargs) -> str:
        """ get python venv path from poetry and set it within config
            beware that Baseconfig._ or cwd kwargs has to be given 
            when current working dir doesn't include a poetry project """

        env:str = cls.poetry("env","info","--path",
            text=True,capture_output=True,**kwargs).stdout.strip()

        if not env:
            raise Exception("Error, no python env found")

        if hasattr(BaseConfig,"_"):

            # allows using 1 config and more                
            BaseConfig._.python_env = env
            BaseConfig._.python_bin = f"{env}/bin/python"
            verbose("set python env:",BaseConfig._.python_env)

        else:
            # for setting python env without config
            BaseConfig.python_env = env
            BaseConfig.python_bin = f"{env}/bin/python"
            verbose("set python env:",BaseConfig.python_env)

        return env

def install(*packages):
    """ easy way for installing whole packages with documentation,
        apt libs, rust libs, node libs, python libs, and files """

    # allow auto config if missing
    try: config = BaseConfig._
    except: config = set_config()

    from sweetheart.install import BaseInstall
    BaseInstall(config).install_packages(*packages)


  #############################################################################
 ## logging functions ########################################################
#############################################################################

def echo(*args,mode:str="default",blank:bool=False):
    """ convenient function for printing admin messages
        the mode attribute must be in blank|logg|exit """

    mode = mode.lower()
    if blank or "blank" in mode: print()

    if "logg" in mode:
        BaseConfig.logg.append(" ".join(args))

    else:
        print("[%s]"% BaseConfig.label.upper(),*args)

    if "exit" in mode: exit()


def verbose(*args,level:int=1):
    """ convenient function for verbose messages 
        level set the intended level of verbosity """

    if BaseConfig.verbosity >= level:
        print(f"sws:{level}:",*args)


def BETA(callable):
    """ decorator for tracking usage of beta code
        indicated when code is not fully tested or fixed 
        code execution is not possible running productive """

    assert not hasattr(BaseConfig,'untrusted_code_forbidden')
    verbose(f"[BETA] {repr(callable)} has been called")
    return callable


def sudo(function):
    """ decorator that allows calling sp.sudo() 
        intends to avoid unwanted uses of sudo """

    def wrapper(*args,**kwargs):
        sp._ALLOW_SUDO_ = '__YES__'
        function(*args,**kwargs)
        del sp._ALLOW_SUDO_

    verbose(f"[SUDO] allow {repr(function)}")
    return wrapper
