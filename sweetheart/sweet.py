"""
sweet.py is the multi-purpose controller of sweetheart
it provides main utilities and the command line interface
"""

from sweetheart.globals import *


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

    # allow altered config
    config.update(values)

    if config.get('run','local') == 'productive':
        config.is_webapp_open = False
        config.is_rethinkdb_local = False
        config.is_jupyter_local = False

    try: init = argv.init
    except: init = False

    if not init:
        # ensure python env setting if not given by subproc_file
        if not hasattr(BaseConfig,'python_env'): sp.set_python_env()
        verbose("python env:",BaseConfig.python_env)
        
    BaseConfig._ = config
    return config


def quickstart(*args,_cli_args=None):

    """ build and run webapp for the current config (autoset if not given)
        usually args should be a HttpServer instance or Route|Mount objects
        however for tests it can be a template or even Html code directly
        Note: this flexibility is provided through mount() method of HttpServer """

    from sweetheart.heart import \
        RethinkDB,JupyterLab,HttpServer

    # allow auto config if missing
    if hasattr(BaseConfig,"_"): config = BaseConfig._
    else: config = set_config()

    if _cli_args:
        # update config from cli
        config.is_webapp_open = not _cli_args.server_only
        config.is_rethinkdb_local = not _cli_args.db_disabled
        config.is_jupyter_local = _cli_args.jupyter_lab
        # config.is_mongodb_local = not _cli_args.db_disabled
        # config.is_cherrypy_local = _cli_args.cherrypy
    
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


def sws(args):
    """ SWeet Shell command line interface """

    try: config = BaseConfig._
    except: raise Exception("Error, config is missing")

    cf,sb = config, config.subproc
    sweet = [config.python_bin,"-m","sweetheart.sweet"]
    vv,py,po = config.python_env,config.python_bin,config.poetry_bin

    if isinstance(args,str): args = args.split()
    if cf.verbosity: sweet.append("-"+"v"*cf.verbosity)

    switch = {
        # sweet.py commands within master project
        'help': [*sweet,"start","-x"],
        # sweet.py command within any project
        'new': [*sweet,"sh","--init","-p",*args[1:]],
        'start': [*sweet,"-p",cf.project,"start",*args[1:]],
        'install': [*sweet,"-p",cf.project,"install",*args[1:]],
        'show': [*sweet,"sh","-p",cf.project,"poetry","show","--tree"],
        # services and utilities commands
        'build-css': [*sb['.tailwindcss'].split()],
        'test': [py,"-m",f"{cf.project}.tests",*args[1:]],
        'jupyter-server': [*sweet,"sh","-p","jupyter","jupyter-server"],
        'notebook': [*sweet,"sh","-p","jupyter","python","-m","jupyter","notebook",*args[1:]],
        # subprocess commands
        'poetry': [config.poetry_bin,*args[1:]],
        'python': [f"{vv}/bin/python",*args[1:]],
        'mdbook': [f"{cf.rust_crates}/mdbook",*args[1:]],
        }

    if args == [] and config.SWSLVL == "1" :
        args= ["echo",f"enjoy programming with Sweetheart!\na bit lost? type 'sws help' for getting help"]

    # autoset the relevant working directory
    cwd= config.PWD
    if args[0]=='poetry': cwd= cf._['module_path']
    elif args[0]=='mdbook': cwd= f"{cf.root_path}/documentation"
    elif args[0]=='build-css': cwd= f"{cf['working_dir']}/resources"

    verbose("working directory:",cwd)
    verbose("invoke shell:"," ".join(switch.get(args[0],args)))

    try: sp.run(*switch.get(args[0],args),cwd=cwd)
    except: verbose("sws has been interrupted")


def install(*packages):
    """ easy way for installing whole packages with documentation,
        apt libs, rust libs, node libs, python libs, and files """

    # allow auto config
    if hasattr(BaseConfig,"_"): config = BaseConfig._
    else: config = set_config()

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

    cli.opt("-V","--version",action="store_true",
        help="provide version info of sweetheart")

    cli.opt("-v","--verbose",action="count",default=0,
        help="get additional messages about on-going process")

    cli.opt("-p",dest="project",nargs=1,
        help="set a project name different of sweetheart")


    # create subparser for the 'shell' command:
    cli.sub("sh",help="the SWeet Shell command line interface")
    cli.set_function(lambda args: sws(args.subargs))

    cli.opt("-V","--version",action="store_true",
        help="provide version info of sweetheart")

    cli.opt("-v","--verbose",action="count",default=0,
        help="get additional messages about on-going process")

    cli.opt("-p",dest="project",nargs=1,
        help="set a project name different of sweetheart")

    cli.opt("--init",action="store_true",
        help="launch init process for building sweetheart ")

    cli.opt("subargs",nargs=cli.REMAINDER,
        help="remaining arguments processed by SWeet Shell")


    # create subparser for the 'start' command:
    cli.sub("start",help="start webapp and the required services")
    cli.set_function(lambda args: quickstart(_cli_args=args))

    cli.opt("-x","--db-disabled",action="store_true",
        help="start without local Database server")

    cli.opt("-j","--jupyter-lab",action="store_true",
        help="start Jupyter Http server for enabling notebooks")

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

    if getattr(argv,"version"):
        from sweetheart import __version__
        print(MASTER_MODULE,__version__)
        exit()
    
    if getattr(argv,"project",None):
        set_config(project=argv.project[0])
    else:
        set_config()

    if getattr(argv,"init",False):
        from sweetheart.install import init
        add_pylibs = getattr(argv,"subargs","")
        init(BaseConfig._, add_pylibs)
    
    cli.apply_function()
