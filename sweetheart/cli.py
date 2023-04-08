"""
cli.py is the multi-purpose controller provided by sweetheart
it provides main utilities through the command line interface
"""

import argparse
from sweetheart import *


class CommandLineInterface:

    def __init__(self) -> None:

        """ build Command Line Interface with ease
            it uses argparse but provides better look and feel """

        # provide default parsers tools
        self.parser= argparse.ArgumentParser()
        self.subparser= self.parser.add_subparsers()
        self.REMAINDER= argparse.REMAINDER
        self.SUPPRESS= argparse.SUPPRESS
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
            exec(f"from sweetheart.services import {classname}")
            eval(f"{classname}.cli_func(args)")

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

    cli.set_function( lambda args:
        print("type 'sws help' for getting some help") )

    cli.opt("-V","--version",action="store_true",
        help="provide version info of sweetheart")

    cli.opt("-v","--verbose",action="count",default=0,
        help="get additional messages about on-going process")

    cli.opt("-p",dest="project",nargs=1,
        help="set a project name different of sweetheart")


    def sws_init(args):
        from sweetheart.install import init
        init(BaseConfig._,add_pylibs=args.subargs)

    #$ sws init
    cli.sub("init",help="launch init process for building sweetheart")
    cli.opt("subargs",nargs=cli.REMAINDER,help="additionnal python modules to install")
    cli.set_function(sws_init)

    #$ sws start
    cli.sub("start",help="start webapp and required services")
    cli.set_service("HttpServer")

    #$ sws test
    cli.sub("test",help="start the given html template as single webpage")
    cli.opt("template",nargs=1,help="filename of the template to test")
    cli.set_function( lambda args: test_template(args.template[0]) )

    #$ sws build-css
    cli.sub("build-css",help="rebuild the tailwind.css file")
    cli.set_function( lambda args: build_css() )
        
    # #$ sws run-jupyter
    # cli.sub("run-jupyter",help="run the JupyterLab server")
    # cli.opt("-o","--open-terminal",action="store_true")
    # cli.set_service("JupyterLab")


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
    
    cli.apply_function()


    # # create subparser for the 'shell' command:
    # cli.sub("sh",help="the SWeet Shell command line interface")
    # cli.set_function(lambda args: sws(args.subargs))

    # cli.opt("-V","--version",action="store_true",
    #     help="provide version info of sweetheart")

    # cli.opt("-v","--verbose",action="count",default=0,
    #     help="get additional messages about on-going process")

    # cli.opt("-p",dest="project",nargs=1,
    #     help="set a project name different of sweetheart")

    # cli.opt("--init",action="store_true",
    #     help="launch init process for building sweetheart ")

    # cli.opt("subargs",nargs=cli.REMAINDER,
    #     help="remaining arguments processed by SWeet Shell")


    # # create subparser for the 'start' command:
    # cli.sub("start",help="start webapp and the required services")
    # cli.set_function(lambda args: quickstart(_cli_args=args))

    # cli.opt("-x","--db-disabled",action="store_true",
    #     help="start without local Database server")

    # cli.opt("-j","--jupyter-lab",action="store_true",
    #     help="start Jupyter Http server for enabling notebooks")

    # # cli.opt("-c","--cherrypy",action="store_true",
    # #     help="start CherryPy Http server for static contents")

    # cli.opt("-s","--server-only",action="store_true",
    #     help="start Http server without opening webbrowser")


    # # create subparser for the 'install' command:
    # cli.sub("install",help="easy way for installing new components")
    # cli.set_function(lambda args: install(*args.packages))

    # cli.opt("packages",nargs="+",
    #     help="names of packages to install: science|web")


    # # create subparsers for services
    # # available only fot the master project
    # cli.sub("rethinkdb-server",help="run the Rethink-Database server")
    # cli.opt("-o","--open-terminal",action="store_true")
    # cli.set_service("RethinkDB")

    # cli.sub("mongodb-server",help="run the Mongo-Database server")
    # cli.opt("-o","--open-terminal",action="store_true")
    # cli.set_service("MongoDB")

    # cli.sub("cherrypy-server",help="run cherrypy as http static server")
    # cli.opt("-o","--open-terminal",action="store_true")
    # cli.set_service("HttpStaticServer")


# def sws(args):
#     """ SWeet Shell command line interface """

#     try: config = BaseConfig._
#     except: raise Exception("Error, config is missing")

#     cf,sb = config, config.subproc
#     sweet = [config.python_bin,"-m","sweetheart.cli"]
#     vv,py,po = config.python_env,config.python_bin,config.poetry_bin

#     if isinstance(args,str): args = args.split()
#     if cf.verbosity: sweet.append("-"+"v"*cf.verbosity)

#     switch = {
#         # sweet.py commands within master project
#         'help': [*sweet,"start","-x"],
#         # sweet.py command within any project
#         'new': [*sweet,"sh","--init","-p",*args[1:]],
#         'start': [*sweet,"-p",cf.project,"start",*args[1:]],
#         'install': [*sweet,"-p",cf.project,"install",*args[1:]],
#         'show': [*sweet,"sh","-p",cf.project,"poetry","show","--tree"],
#         # services and utilities commands
#         'build-css': [*sb['.tailwindcss'].split()],
#         'test': [py,"-m",f"{cf.project}.tests",*args[1:]],
#         'jupyter-server': [*sweet,"sh","-p","jupyter","jupyter-server"],
#         'notebook': [*sweet,"sh","-p","jupyter","python","-m","jupyter","notebook",*args[1:]],
#         # subprocess commands
#         'poetry': [config.poetry_bin,*args[1:]],
#         'python': [f"{vv}/bin/python",*args[1:]],
#         'mdbook': [f"{cf.rust_crates}/mdbook",*args[1:]],
#         }

#     if args == [] and config.SWSLVL == "1" :
#         args= ["echo",f"enjoy programming with Sweetheart!\na bit lost? type 'sws help' for getting help"]

#     # autoset the relevant working directory
#     cwd= config.PWD
#     if args[0]=='poetry': cwd= cf.module_path
#     elif args[0]=='mdbook': cwd= f"{cf.root_path}/documentation"
#     elif args[0]=='build-css': cwd= f"{cf.working_dir}/resources"

#     verbose("working directory:",cwd)
#     verbose("invoke shell:"," ".join(switch.get(args[0],args)))

#     try: sp.shell(*switch.get(args[0],args),cwd=cwd)
#     except: verbose("sws has been interrupted")

