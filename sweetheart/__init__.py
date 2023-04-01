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
    # set sws level into environment 
    SWSLVL = os.environ['SWSLVL'] = f"{int(os.getenv('SWSLVL','0'))+1}"
    assert int(SWSLVL) <= 2

    # default path settings
    poetry_bin = f"{HOME}/.local/bin/poetry"
    python_bin = sys.executable # no python env set here
    rust_crates = f"{HOME}/.cargo/bin"

    # default productive settings
    async_host = "http://127.0.0.1:8000"# uvicorn
    database_host = "rethinkdb://127.0.0.1:28015"
    database_admin = "http://127.0.0.1:8180"
    jupyter_host = "http://127.0.0.1:8888"
    nginxunit_host = "http://localhost"

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
            'unit_listener': "*:80",
            'python_version': "3.10",# for setting Nginx Unit
            'node_version': "16.x",# for getting node from nodesource.com
            'system_dir': "/etc/systemd/system",

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

    def load_json(self,subproc:bool=False):
        """ update config object from given json file """

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


def set_config(
    values:dict = {},
    project:str = MASTER_MODULE,
    config_file:str = None ) -> BaseConfig :

    """ set or reset sweetheart configuration with ease
        allow working with different projects and configs 
        
        >>> config = set_config({
        >>>     "run": "local",
        >>>     "db_name": "test",
        >>>     "db_path": "~/my_database/location" }) """

    config = BaseConfig(project)

    if config_file:
        config.config_file = config_file

    elif isinstance(values,str):
        # allow catching config_file instead of values
        if os.path.isfile(values) and values[:-5]==".json":
            config.config_file = config_file = values

    # update config from json conf file
    try: config.load_json(subproc=True)
    except: echo("WARNING: json config files loading failed")

    # then change config from given values
    config.update(values)

    # provide shortcut for setting running env
    if config.get('run','local') == 'productive':
        config.is_webapp_open = False
        config.is_rethinkdb_local = False
        config.is_jupyter_local = False

    if "init" not in sys.argv :
        # ensure python env setting if not given by subproc_file
        if not hasattr(BaseConfig,'python_env'): sp.set_python_env()
        verbose("python env:",BaseConfig.python_env)
        
    BaseConfig._ = config
    return config


def quickstart(*args,_cli_args=None):

    """ build and run webapp for the current config (autoset when not given)
        usually args should be a HttpServer instance or Route|Mount objects
        however for tests it can be a template or even Html code directly
        NOTE: this flexibility is provided by mount() method of HttpServer """

    from sweetheart.services import \
        RethinkDB,JupyterLab,HttpServer

    # allow auto config if missing
    if hasattr(BaseConfig,"_"): config = BaseConfig._
    else: config = set_config()

    if _cli_args:
        # update config from cli
        config.is_webapp_open = not _cli_args.server_only
        config.is_rethinkdb_local = not _cli_args.db_disabled
        config.is_jupyter_local = _cli_args.jupyter_lab
    
    if config.is_jupyter_local:
        # set and run Jupyterlab server
        JupyterLab(config,run_local=True)

    if args and isinstance(args[0],HttpServer):
        # set webapp from given HttpServer instance
        webapp = args[0]
        if hasattr(args[0],'data'): args[0].mount(*args[1:])
    else:
        # build new webapp from Route|Mount objects,html code or template
        webapp = HttpServer(config)
        if config.is_rethinkdb_local:
            # set and run RethinkDB server
            webapp.database = RethinkDB(config,run_local=True)
            webapp.database.set_websocket()
            webapp.database.set_client()
        webapp.mount(*args)
        
    # start webapp within current bash
    webapp.run_local(service=False)


  #############################################################################
 ## HTML handling ############################################################
#############################################################################

def HTMLTemplate(filename:str,**kwargs):
    """ provide a Starlette-like function for rendering templates
        including configuration data and some python magic stuff """

    from sweetheart.bottle import SimpleTemplate
    from starlette.responses import HTMLResponse

    # if not hasattr(BaseConfig,"_"):
    #     verbose("config is missing and autoset by HTMLTemplate")
    #     set_config()

    # set templates dir as working dir
    os.chdir(BaseConfig._.working_dir)

    if os.path.isfile(f"{BaseConfig._.templates_dir}/{filename}"):
        # load template from filename if exists
        with open(f"{BaseConfig._.templates_dir}/{filename}","r") as tpl:
            template = tpl.read()

    elif isinstance(filename,str):
        # alternatively test the given string as template
        template = filename

    else: raise TypeError

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

    try: select = BaseConfig._['webbrowser']
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
            # allow shell("echo","hello") instead of shell(["echo","hello"])
            return cls.run(args,**kwargs)

    @classmethod
    def read_sh(cls,script:str):
        """ excec line by line a long string as a shell script """

        for instruc in script.splitlines():
            cls.run(instruc.strip(),shell=True)

    @classmethod
    def sudo(cls,*args,**kwargs):
        """ a Jupyter compliant sudo cmd that runs sudo -S """

        command = ' '.join(args)

        if getattr(cls,'_getpass_',False) is True: 
            sp.shell(f"sudo -S {command}")
        else:
            sp.shell(f"echo {os.getpass()} | sudo -S {command}")
            cls._getpass_ = True


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

        return cls.shell(BaseConfig.poetry_bin,*args,**kwargs)

    @classmethod
    def python(cls,*args,**kwargs):

        # no python env given is forbidden here
        assert hasattr(BaseConfig,'python_env')
        return cls.shell(BaseConfig.python_bin,*args,**kwargs)

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
        verbose("set python env:",BaseConfig.python_env)


def install(*packages):
    """ easy way for installing whole packages with documentation,
        apt libs, rust libs, node libs, python libs, and files """

    # allow auto config
    if hasattr(BaseConfig,"_"): config = BaseConfig._
    else: config = set_config()

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
        print(f"sws:{BaseConfig.SWSLVL}:",*args)

