"""
sweet.py is the multi-purpose controller of sweetheart
it provides cli, install process, sandbox and services
"""
from sweetheart.globals import *


def set_config(

    values:dict = {},
    project:str = SWEETHEART,
    config_file:str = None ) -> BaseConfig:

    """ set or reset sweetheart configuration 
        allow working with differents projects and configs """

    from sys import argv

    global config
    config = BaseConfig(project)
    if config_file: config.config_file = config_file

    try: 
        # update config from given json file
        with open(config.config_file) as fi:
            config.update(json.load(fi))
            verbose("config file:",config.config_file)
    except: pass

    # allow altered config
    config.update(values)

    try: 
        # get subproc settings from given json file
        with open(config.subproc_file) as fi:
            subproc_settings = json.load(fi)
            verbose("subproc file:",config.subproc_file)

        # fix updatable subproc settings here
        for key in ('pyenv','rustpath','codepath','mongopath'):

            value = subproc_settings.get(key)
            if value and key == 'pyenv': 
                BaseConfig.python_env = value
                BaseConfig.python_bin = f"{value}/bin/python"
            elif value:
                config.subproc[key] = value
    except: pass

    # ensure python subprocess
    if not '--init' in argv and\
        not hasattr(BaseConfig,'python_env'):
            sp.set_python_env()

    BaseConfig._ = config
    return config


def webbrowser(url:str):
    """ start url within webbrowser set in config """

    try: select = config['webbrowser']
    except: select = None

    if select and config.subproc.get(select):
        sp.shell(config.subproc[select]+url)

    elif BaseConfig.WSL_DISTRO_NAME:
        sp.shell(config.subproc['msedge.exe']+url)

    else: sp.run(BaseConfig.python_bin,"-m","webbrowser","url")


def quickstart(*args,_cli_args=None):
    """ build and run webapp for the existing config """

    try: assert 'config' in globals()
    except: set_config()

    # set config from cli if given
    if _cli_args:
        config.is_webapp_open = not _cli_args.server_only
        config.is_mongodb_local = not _cli_args.mongo_disabled
        config.is_jupyter_local = _cli_args.jupyter_lab
        config.is_cherrypy_local = _cli_args.cherrypy
    
    # run Jupyterlab server
    if config.is_jupyter_local:
        from sweetheart.heart import Notebook
        Notebook(config,run_local=True)

    # run CherryPy server
    if config.is_cherrypy_local:
        from sweetheart.heart import StaticServer
        StaticServer(config,run_local=True)

    # run MongoDB server
    if config.is_mongodb_local:
        from sweetheart.heart import Database
        sp.mongo = Database(config,run_local=True)

    # build and start webapp
    from sweetheart.heart import HttpServer
    if args and isinstance(args[0],HttpServer):
        # allow tests within JupyterLab
        args[0].mount(*args[1:],open_with=webbrowser)
        args[0].run_local(service=False)
    else:
        webapp = HttpServer(config)
        webapp.mount(*args,open_with=webbrowser)
        webapp.run_local(service=False)


def sws(args):
    """ SWeet Shell command line interface """

    try: assert 'config' in globals()
    except: raise Exception("Error, config is missing")

    if isinstance(args,str): args = args.split()
    cf,sb = config, config.subproc
    sw = [config.python_bin,"-m","sweetheart.sweet"]
    vv,py,po = config.python_env,config.python_bin,config.poetry_bin

    switch = {
        'python': [f"{vv}/bin/ipython",*args[1:]],
        'poetry': [config.poetry_bin,*args[1:]],
        'mdbook': [f"{sb['rustpath']}/mdbook",*args[1:]],
        'sweet': [py,"-m","sweetheart.sweet",*args[1:]],
        'start': [py,"-m","sweetheart.sweet","start",*args[1:]],
        'init': [*sw,"-p",args[1],"--init",*args[2:]],
        'install': [py,"-m","sweetheart.sweet","install",*args[1:]],
        'jupyter': [py,"-m","jupyterlab","--no-browser",*args[1:]],
        }

    if args[0]=='poetry': cwd= cf.subproc['codepath']
    elif args[0]=='mdbook': cwd= f"{cf.root_path}/documentation"
    else: cwd= config.PWD

    verbose("cwd:",cwd)
    try: sp.run(*switch.get(args[0],args),cwd=cwd)
    except: echo("sws has been interrupted")


def install(*packages):

    try: assert 'config' in globals()
    except: raise Exception("Error, config is missing")

    from sweetheart.install import BaseInstall
    BaseInstall(config).install_packages(*packages)


class CommandLineInterface:

    def __init__(self) -> None:
        """ build Command Line Interface with ease
            it uses argparse but provides better look and feel """

        # provide default parsers tools
        import argparse
        self.parser= argparse.ArgumentParser()
        self.subparser= self.parser.add_subparsers()
        self.REMAINDER = argparse.REMAINDER
        self.dict= { "_": self.parser }
        self.cur= "_"
    
    def opt(self,*args,**kwargs):
        self.dict[self.cur].add_argument(*args,**kwargs)

    def sub(self,*args,**kwargs):
        self.cur = args[0]
        self.dict[args[0]] = self.subparser.add_parser(*args,**kwargs)
    
    def set_function(self,func):
        """ set related function for the current parser or subparser """
        self.dict[self.cur].set_defaults(func=func)

    def set_service(self,classname:str):
        """ set related service for the current parser or subparser """

        def func(args):
            exec(f"from sweetheart.heart import {classname}")
            eval(f"{classname}(config).cli_func(args)")

        self.dict[self.cur].set_defaults(func=func)

    def set_parser(self):
        self.args = self.parser.parse_args()
        return self.args


if __name__ == "__main__":

    # build sweetheart command iine interface
    cli = CommandLineInterface()
    cli.set_function(lambda args:
        echo("type 'sws sweet --help' for getting some help"))

    cli.opt("-v","--verbose",action="count",default=0,
        help="get additional messages about on-going process")

    cli.opt("-p",dest="project",nargs=1,
        help="set a project name different of sweetheart")

    cli.opt("-i","--init",action="store_true",
        help="launch init process for building new sweetheart project")


    # create subparser for the 'start' command:
    cli.sub("start",help="start webapp and the required services")
    cli.set_function(lambda args: quickstart(_cli_args=args))

    cli.opt("-x","--mongo-disabled",action="store_true",
        help="start without local Mongo Database server")

    cli.opt("-j","--jupyter-lab",action="store_true",
        help="start JupyterLab Http server for enabling notebooks")

    cli.opt("-c","--cherrypy",action="store_true",
        help="start CherryPy Http server for static contents")

    cli.opt("-s","--server-only",action="store_true",
        help="start Http server without opening webbrowser")


    # create subparser for the 'shell' command:
    cli.sub("shell",help="the SWeet Shell command line interface")
    cli.set_function(lambda args: sws(args.subargs))

    cli.opt("subargs",nargs=cli.REMAINDER,
        help="remaining arguments processed by SWeet Shell")

    # create subparser for the 'install' command:
    cli.sub("install",help="easy way for installing new components")
    cli.set_function(lambda args: install(*args.packages))

    cli.opt("packages",nargs="+",
        help="names of packages to install: science|web")


    # create subparsers for services
    cli.sub("mongodb-server",help="run the Mongo Database server")
    cli.opt("-o","--open-terminal",action="store_true")
    cli.set_service("Database")

    cli.sub("jupyter-server",help="run the JupyterLab server")
    cli.opt("-o","--open-terminal",action="store_true")
    cli.set_service("Notebook")

    cli.sub("cherrypy-server",help="run cherrypy as http static server")
    cli.opt("-o","--open-terminal",action="store_true")
    cli.set_service("StaticServer")


    # execute command line arguments
    argv = cli.set_parser()
    BaseConfig.verbosity = argv.verbose

    if getattr(argv,"project",None):
        set_config(project=argv.project[0])
    else:
        set_config()

    if argv.init:
        from sweetheart.install import init
        init(config)

    argv.func(argv)
