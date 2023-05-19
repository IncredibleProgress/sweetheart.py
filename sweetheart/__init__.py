"""
SWEETHEART 0.1.x 'new age rising'
rock-solid pillars for building innovative enterprise-grade apps

Start from scratch and create with ease and efficiency the apps you really need
embedding reliable open-source code, highest quality components, best practices.

Foreword
    I'm happy that you look interested by the Sweetheart project.
    I spent many hours on my free time to provide the best of what coding can offer.
    I thank a lot my wife and my children also very much for their understanding and long patience.
    Now discover what you can really do with computers and furthermore at the light speed!

About __init__.py :
    imports python modules: sys, json
    provides: set_config, quickstart, TemplateResponse
    the python os module is replaced by an os class
    (non-exhaustive)

About stemplate.py
    this currently includes an adapted version of bottle.py,
    which is not part of the sweetheart project itself. Info:
        Homepage and documentation: http://bottlepy.org/
        Copyright (c) 2016, Marcel Hellkamp.
        License: MIT (see LICENSE for details)
"""

import re,sys,json
from collections import UserDict
from sweetheart.subprocess import os

__version__ = "0.1.2"
__license__ = "CeCILL-C FREE SOFTWARE LICENSE AGREEMENT"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"

# default dir and module name of master project
#FIXME: allow replacing sweetheart by a fork of it
MASTER_MODULE = "sweetheart"


class BaseConfig(UserDict):
    """ configuration settings base class

        use the get_config() func for getting a new instance 
        BaseConfig._ returns the last config created with it """

    # stdout messages settings
    verbosity = 0
    label = MASTER_MODULE # printed with echo()

    # get environment settings
    HOME = os.path.expanduser('~')
    LANG = os.getlocale()[0].split('_')[0]
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
            "nginxunit_host": "http://localhost:80",

            # default low level settings
            # can be updated using load_json(subproc=True)
            'systemd': [],
            'stsyntax': r"<% %> % {% %}",
            'python_version': "3.10",# used for setting Nginx Unit
            'node_version': "16.x",# used getting node from nodesource.com

            # can not be updated within load_json(subproc=True)
            # the settings are locked because key starts with .
            '.msedge.exe': "cmd.exe /c start msedge --app=",
            '.brave.exe': f"cmd.exe /c start brave --app=",
            '.tailwindcss': "npx tailwindcss -i tailwind.base.css -o tailwind.css" }

        self.data = {
            # editable general settings
            "db_name": "test",
            "app_module": "start",# no .py suffix here
            "app_callable": "webapp",
            "templates_base": "HTML_BASE",
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
                "load": "pylibs tailwind vue+reql",
                "debug": 1,# brython() debug argument
            },
            "static_files": {
                '/favicon.ico': "resources/favicon.ico",
                '/tailwind.css': "resources/tailwind.css",
                '/vue.js': "resources/node_modules/vue/dist/vue.global.prod.js",
            },
            "static_dirs": {
                '/resources': f"resources",
                '/documentation': "sweetdoc",
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
        # _old must be set by set_config()
        assert hasattr(BaseConfig,'_old')
        return self

    def __exit__(self,exc_type,exc_value,exc_tb):

        if BaseConfig._old is not None:
            # this recovers a pre-existing config
            # None value is set within set_config()
            BaseConfig._ = BaseConfig._old
        
        del BaseConfig._old
        
    def load_json(self,subproc:bool=False):
        """ update config object from given json file(s) """

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
    BaseConfig._old = getattr(BaseConfig,'_',None)
    config = BaseConfig._ = BaseConfig(project)

    if config_file:
        config.config_file = config_file

    elif isinstance(values,str):
        # allow catching config_file instead of values
        if os.path.isfile(values) and values[:-5]==".json":
            config.config_file = config_file = values

    # update config from json conf file
    try: config.load_json(subproc=True)
    except: echo("WARN: failed loading json config files")

    if "init" not in sys.argv :
        # ensure python env setting when not given by subproc_file
        try: config.python_env
        except: sp.set_python_env()

    # provide shortcut for setting running env
    if values.get('run'):

        config.run = values['run']
        assert config.run in "testing|productive"
        del values['run']#! avoid confusion

        if config.run == "productive":

            config.is_webapp_open = False
            config.is_rethinkdb_local = False
            config.is_jupyter_local = False
            #FIXME: productive settings not fully implemented
            echo("WARN: !! run productive not yet available !!")
            BaseConfig.untrusted_code_forbidden = True

    # update config and return
    config.update(values)
    return config


def quickstart(*args,_cli_args=None):

    """ build and run webapp for the current config (autoset when not given)
        usually args should be a HttpServer instance or Route|Mount objects
        however for tests it can be a template or even Html code directly
        NOTE: this flexibility is provided by the mount() method of HttpServer """

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
        with set_config(project="jupyter") as cfg:
            jupy = JupyterLab(cfg)
            try: jupy.run_local(service='jupyterlab')
            except: jupy.run_local(terminal=True)

    if args and isinstance(args[0],HttpServer):
        # set webapp from a given HttpServer instance
        webapp = args[0]
    else:
        # build new webapp from Route|Mount objects,html code or template
        webapp = HttpServer(config,set_database=config.is_rethinkdb_local)
        webapp.mount(*args)
    
    #FIXME: start webapp within current bash
    webapp.run_local(service=None,terminal=None)


  #############################################################################
 ## HTML handling ############################################################
#############################################################################

class HtmlTemplate:
    
    pscript  = """
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
    window.createVueApp(json.dumps(dict))\n"""

    def __init__(self,config:BaseConfig):

        self.config = config

        self.path =\
            f"{config.working_dir}/{config.templates_dir}"

        self.html_overwrite = {
            # provide magic syntax <!SWEETHEART html>
            f'<!{MASTER_MODULE.upper()} html>': \
                f'%rebase("{config.templates_base}")',
            # provide magic html facilities
            '<vue': '<div v-cloak id="VueApp"',
            '</vue>': '</div>',
            # provide magic <python></python> syntax
            '<python>': f'<script type="text/python">{self.pscript}',
            '</python>': '</script>' }

    def render(self,filename):

        from sweetheart.stemplate import template

        with open(f"{self.path}/{filename}") as tpl:
            template_string = tpl.read()

        # html injection forbidden in template_string
        tok1,tok2 = self.config.stsyntax[-2:]
        if re.search(tok1+r" *!.* *"+tok2,template_string):
            raise Exception("html injection using !value is not allowed")

        for old,new in self.html_overwrite.items():
            #TODO: use regex instead of str replacements
            template_string= template_string.replace(old,new)

        return template(
            template_string,
            # enforced default values
            __lang__ = self.config.LANG,
            __dbnm__ = self.config.db_name,
            __host__ = self.config.nginxunit_host,
            # allow setting custom values
            **self.config.templates_settings )

    def run_for_test(self,filename,build_css=True):

        from starlette.routing import Route
        from starlette.responses import HTMLResponse
        
        self.config.verbosity = 1
        self.config.is_webapp_open = True
        self.config.is_rethinkdb_local = False
        self.config.is_jupyter_local = False

        if build_css:
            sp.shell(self.config.subproc['.tailwindcss'],
                cwd=f"{self.config.working_dir}/resources")

        content = HtmlTemplate(self.config).render(filename)
        quickstart( Route("/",HTMLResponse(content)) )


def TemplateResponse(filename):

    from starlette.responses import HTMLResponse

    try: config = BaseConfig._
    except: config = set_config()
        
    content = HtmlTemplate(config).render(filename)
    return HTMLResponse(content)


def webbrowser(url:str):
    """ start url within the webbrowser set in config 
        it allows running on the WSL with Windows 10/11 """

    try: select = BaseConfig._.webbrowser
    except: select = None

    if select and '.'+select in BaseConfig._.subproc:
        sp.shell(f"{BaseConfig._.subproc['.'+select]}{url}")

    elif BaseConfig._.WSL_DISTRO_NAME:
        sp.shell(f"{BaseConfig._.subproc['.msedge.exe']}{url}")

    else: sp.python("-m","webbrowser",url)


  #############################################################################
 ## Subprocesses handling ####################################################
#############################################################################

class sp:
    """ namespace providing basic subprocess features 
        beware that it uses BaseConfig and not config """

    shell = os.shell
    stdout = os.stdout

    @classmethod
    def sudo(cls,*args,**kwargs):
        """
        a Jupyter compliant sudo cmd that runs sudo -S
        this asks sudo password with new or expired sudo session
        in this case text and input arguments can not be given
        """

        #NOTE:
        # shell-like syntax sp.sudo("apt-get install nginx") not allowed 

        assert getattr(cls,'_ALLOW_SUDO_','__NO__') == '__YES__'
        passwd_ok= cls.shell("sudo","-n","true",stderr=os.DEVNULL).returncode
        
        if passwd_ok:
            # don't ask for the sudo password here
            return cls.shell("sudo","-S",*args,**kwargs)
        else: 
            # text and input arguments can not be given here
            assert 'text' not in kwargs
            assert 'input' not in kwargs

            return cls.shell("sudo","-S",*args,text=True,
                input=os.getpass("sudo passwd required: "),**kwargs)

    @classmethod
    def systemctl(cls,*args,**kwargs):

        """ exec the systemctl shell cmd with sudo and
            doesn't require allowing sudo previously with @sudo
            this allows doing a 'single shot' within Jupyter """

        hold = getattr(cls,'_ALLOW_SUDO_ ',None)
        cls._ALLOW_SUDO_ = '__YES__'
        cls.sudo("systemctl",*args,**kwargs)
        if hold: cls._ALLOW_SUDO_ = hold
        else: del cls._ALLOW_SUDO_

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
    def terminal(cls,cmd:str,select:str,**kwargs) -> os.Process:
        """ run cmd within selected terminal 
            select must be in xterm|winterm|wsl """

        assert select in "xterm|winterm|wsl"
        
        wsl = f"cmd.exe /c start wsl {cmd}"
        winterm = f"cmd.exe /c start wt wsl {cmd}"
        xterm = f"xterm -C -geometry 190x19 -e {cmd}"
        
        cmd = eval(select)
        kwargs['stdout'] = os.DEVNULL

        process = os.Process(target=lambda:cls.shell(cmd,**kwargs))
        process.start()

        return process
    
    @classmethod
    def poetry(cls,*args,**kwargs):

        if not kwargs.get('cwd') and hasattr(BaseConfig,'_'):
            #FIXME: doesn't work within jupyter
            kwargs['cwd'] = BaseConfig._['module_path']
            verbose("poetry cwd:",kwargs['cwd'])

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

        if hasattr(BaseConfig,'_'):

            # allows using 1 config and more                
            BaseConfig._.python_env = env
            BaseConfig._.python_bin = f"{env}/bin/python"
            verbose("python env:",BaseConfig._.python_env)

        else:
            # for setting python env without config
            BaseConfig.python_env = env
            BaseConfig.python_bin = f"{env}/bin/python"
            verbose("BaseConfig.python_env:",BaseConfig.python_env)

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

def echo(*args,blank=False):
    """ convenient function for printing admin messages """

    if blank: print()
    print(f"[{BaseConfig.label.upper()}]",*args)


def verbose(*args,level:int=1):
    """ convenient function for verbose messages 
        level set the intended level of verbosity """

    if BaseConfig.verbosity >= level:
        print(f"sws:{level}:",*args)


def beta(callable):
    """ @decorator for tracking usage of beta code
        indicated when code is not fully tested or fixed 
        code execution is not possible running productive """

    assert not hasattr(BaseConfig,'untrusted_code_forbidden')
    verbose(f"[BETA] {repr(callable)} has been called")
    return callable


def sudo(function):
    """ @decorator that allows calling sp.sudo() 
        intends to avoid unwanted uses of sudo """

    def wrapper(*args,**kwargs):
        sp._ALLOW_SUDO_ = '__YES__'
        function(*args,**kwargs)
        del sp._ALLOW_SUDO_

    verbose(f"[SUDO] exec: {repr(function)}")
    return wrapper
