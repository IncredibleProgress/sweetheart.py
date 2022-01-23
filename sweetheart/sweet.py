"""
sweet.py is the multi-purpose controller of sweetheart
it provides cli, install process, sandbox and services
"""
from sweetheart.globals import *


def set_config(

    values:dict = {},
    project:str = MASTER_MODULE,
    sandbox:bool = False,
    config_file:str = None ) -> BaseConfig:

    """ set or reset sweetheart configuration 
        allow working with differents projects and configs """

    config = BaseConfig(project)
    if config_file: config.config_file = config_file

    if sandbox is False:
        # disable sandbox settings
        config.is_webapp_open = False
        config.is_rethinkdb_local = False
        config.is_jupyter_local = False
        # config.is_mongodb_local = False
        # config.is_cherrypy_local = False

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
        for key,value in subproc_settings.items():

            if key.startswith('.'): 
                echo(f"WARNING: update of subproc setting '{key}' forbidden")
                continue

            if value and key == 'pyenv': 
                BaseConfig.python_env = value
                BaseConfig.python_bin = f"{value}/bin/python"
            elif value:
                config.subproc[key] = value
    except: pass

    try: not_init = not argv.init
    except: not_init = True

    # ensure python subprocess setting
    if not_init:
        if not hasattr(BaseConfig,'python_env'): sp.set_python_env()
        verbose("python env:",BaseConfig.python_env)
        
    BaseConfig._ = config
    return config


def quickstart(*args,_cli_args=None):
    """ build and run webapp for the existing config """

    from sweetheart.heart import RethinkDB,JupyterLab,HttpServer

    # allow auto config
    if hasattr(BaseConfig,"_"): config = BaseConfig._
    else: config = set_config(sandbox=True)

    # set config from cli if given
    if _cli_args:
        config.is_webapp_open = not _cli_args.server_only
        config.is_rethinkdb_local = not _cli_args.db_disabled
        config.is_jupyter_local = _cli_args.jupyter_lab
        # config.is_mongodb_local = not _cli_args.db_disabled
        # config.is_cherrypy_local = _cli_args.cherrypy
    
    # set and run Jupyterlab server
    if config.is_jupyter_local:
        JupyterLab(config,run_local=True)

    # set and run RethinkDB server
    if config.is_rethinkdb_local:
        RethinkDB(config,run_local=True)

    # # run CherryPy server
    # if config.is_cherrypy_local: 
    #     HttpStaticServer(config,run_local=True)

    # # run MongoDB server
    # if config.is_mongodb_local:
    #     MongoDB(config,run_local=True)

    # build and start webapp
    if args and isinstance(args[0],HttpServer):
        if hasattr(args[0],'data'): args[0].mount(*args[1:])
        args[0].run_local(service=False)
    else:
        webapp = HttpServer(config).mount(*args)
        webapp.run_local(service=False)


def sws(args):
    """ SWeet Shell command line interface """

    try: config = BaseConfig._
    except: raise Exception("Error, config is missing")

    if isinstance(args,str): args = args.split()
    cf,sb = config, config.subproc
    sweet = [config.python_bin,"-m","sweetheart.sweet"]
    if cf.verbosity: sweet.append("-"+"v"*cf.verbosity)
    vv,py,po = config.python_env,config.python_bin,config.poetry_bin

    switch = {
        # sweet.py commands within master project
        'help': [*sweet,"start","-x"],
        'rethinkdb-server': [*sweet,"rethinkdb-server",*args[1:]],
        # sweet.py command within any project
        'start': [*sweet,"-p",cf.project,"start",*args[1:]],
        'install': [*sweet,"-p",cf.project,"install",*args[1:]],
        'new': [*sweet,"sh","--init","-p",*args[1:]],
        #FIXME: services and utilities commands
        'test': [py,"-m",f"{cf.project}.tests",*args[1:]],
        'build-css': [*config.subproc['.tailwindcss'].split()],
        #FIXME: subprocess commands
        'po': [config.poetry_bin,*args[1:]],
        'py': [f"{vv}/bin/ipython",*args[1:]],
        'md': [f"{sb['rustpath']}/mdbook",*args[1:]],
        'poetry': [config.poetry_bin,*args[1:]],
        'python': [f"{vv}/bin/ipython",*args[1:]],
        'mdbook': [f"{sb['rustpath']}/mdbook",*args[1:]],
        }

    if args == []:
        commands = " ".join(list(switch))
        args = ["echo",f"\nsws available commands:\n  {commands}\n"]

    #FIXME: autoset relevant working directory
    if args[0]=='po' or args[0]=='poetry': cwd= cf.subproc['codepath']
    elif args[0]=='md' or args[0]=='mdbook': cwd= f"{cf.root_path}/documentation"
    elif args[0]=='build-css': cwd= f"{cf['working_dir']}/resources"
    else: cwd= config.PWD

    verbose("working directory:",cwd)
    verbose("invoke shell:"," ".join(switch.get(args[0],args)),level=2)

    try: sp.run(*switch.get(args[0],args),cwd=cwd)
    except: echo("sws has been interrupted")


def install(*packages):
    """ an easy way for installing any packages """

    # allow auto config
    if hasattr(BaseConfig,"_"): config = BaseConfig._
    else: config = set_config(sandbox=True)

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
        self.SUPPRESS = argparse.SUPPRESS
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
            eval(f"{classname}(BaseConfig._).cli_func(args)")

        self.dict[self.cur].set_defaults(func=func)

    def set_parser(self):
        self.args = self.parser.parse_args()
        return self.args

    def apply_function(self):
        """ apply related function defined with set_function and set_service """
        self.args.func(self.args)


if __name__ == "__main__":

    # build sweetheart command iine interface
    cli = CommandLineInterface()
    cli.set_function(lambda args:
        echo("type 'sws help' for getting some help"))

    cli.opt("-v","--verbose",action="count",default=0,
        help="get additional messages about on-going process")

    cli.opt("-p",dest="project",nargs=1,
        help="set a project name different of sweetheart")


    # create subparser for the 'shell' command:
    cli.sub("sh",help="the SWeet Shell command line interface")
    cli.set_function(lambda args: sws(args.subargs))

    cli.opt("-v","--verbose",action="count",default=0,
        help="get additional messages about on-going process")

    cli.opt("-p",dest="project",nargs=1,
        help="set a project name different of sweetheart")

    cli.opt("--init",action="store_true",
        help="launch init process for building sweetheart ")

    # cli.opt("-a","--add",dest="pylibs",nargs="+",
    #     help="list extra python modules to install")

    cli.opt("subargs",nargs=cli.REMAINDER,
        help="remaining arguments processed by sweet shell")


    # create subparser for the 'start' command:
    cli.sub("start",help="start webapp and the required services")
    cli.set_function(lambda args: quickstart(_cli_args=args))

    cli.opt("-x","--db-disabled",action="store_true",
        help="start without local Database server")

    cli.opt("-j","--jupyter-lab",action="store_true",
        help="start JupyterLab Http server for enabling notebooks")

    # cli.opt("-c","--cherrypy",action="store_true",
    #     help="start CherryPy Http server for static contents")

    cli.opt("-s","--server-only",action="store_true",
        help="start Http server without opening webbrowser")


    # create subparser for the 'install' command:
    cli.sub("install",help="easy way for installing new components")
    cli.set_function(lambda args: install(*args.packages))

    cli.opt("packages",nargs="+",
        help="names of packages to install: science|web")


    # create subparsers for services
    # available only fot the master project
    cli.sub("rethinkdb-server",help="run the Rethink-Database server")
    cli.opt("-o","--open-terminal",action="store_true")
    cli.set_service("RethinkDB")

    cli.sub("jupyter-server",help="run the JupyterLab server")
    cli.opt("-o","--open-terminal",action="store_true")
    cli.set_service("JupyterLab")

    # cli.sub("mongodb-server",help="run the Mongo-Database server")
    # cli.opt("-o","--open-terminal",action="store_true")
    # cli.set_service("MongoDB")

    # cli.sub("cherrypy-server",help="run cherrypy as http static server")
    # cli.opt("-o","--open-terminal",action="store_true")
    # cli.set_service("HttpStaticServer")


    # execute command line arguments
    argv = cli.set_parser()
    BaseConfig.verbosity = getattr(argv,"verbose",0)

    if getattr(argv,"project",None): set_config(project=argv.project[0])
    else: set_config()

    if getattr(argv,"init",False):
        from sweetheart.install import init
        add_pylibs = getattr(argv,"subargs","")
        init(BaseConfig._, add_pylibs)
    
    cli.apply_function()
