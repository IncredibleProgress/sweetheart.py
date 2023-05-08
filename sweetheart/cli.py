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

    # def set_service(self,classname:str):
    #     """ set related service for the current parser or subparser """

    #     def func(args):
    #         exec(f"from sweetheart.services import {classname}")
    #         eval(f"{classname}(BaseConfig._).cli_func(args)")

    #     self.dict[self.cur].set_defaults(func=func)

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

    cli.opt("-t","--open-terminal",action="store_true",
        help="executes command within a detached terminal window if available")

    cli.opt("-p",dest="project",nargs=1,
        help="set a project name different of sweetheart")


    def sws_init(args):
        from sweetheart.install import init
        init(BaseConfig._,add_pylibs=args.pylibs)

    #$ sws init
    cli.sub("init",help="launch init process for building sweetheart")
    cli.opt("pylibs",nargs=cli.REMAINDER,help="additionnal python modules to install")
    cli.set_function(sws_init)

    #$ sws test
    cli.sub("test",help="start the given html template as single webpage")
    cli.opt("template",nargs=1,help="filename of the template to test")
    cli.set_function( lambda args: test_template(args.template[0]) )

    #$ sws build-css
    cli.sub("build-css",help="rebuild the tailwind.css file")
    cli.set_function( lambda args: build_css() )

    
    def sws_start(args):

        service = args.service.lower()

        if args.systemd and service == 'jupyter':
            sp.systemctl("reload-or-restart jupyterlab")
            # from sweetheart.services import JupyterLab
            # JupyterLab(BaseConfig._).run_local(service='jupyterlab')

        elif service == 'jupyter': 
            from sweetheart.services import JupyterLab
            JupyterLab(BaseConfig._).run_local(terminal=args.open_terminal)

        elif service == 'quickstart':
            quickstart(_cli_args=args)

        else: raise NotImplementedError

    #$ sws start
    cli.sub("start",help="start webapp and required services")
    cli.set_function(sws_start)

    cli.opt("-S","--systemd",action="store_true",
        help="restart-or-reload the service for production via systemd")

    cli.opt("-x","--db-disabled",action="store_true",
        help="start without local Database server")

    cli.opt("-j","--jupyter-lab",action="store_true",
        help="start Jupyter Http server for enabling notebooks")

    cli.opt("-s","--server-only",action="store_true",
        help="start Http server without opening webbrowser")

    cli.opt("service",nargs="?",default="quickstart",
        help="provide here the nickname of the service to start")


    # execute command line arguments
    argv = cli.set_parser()
    BaseConfig.verbosity = getattr(argv,"verbose",0)

    if getattr(argv,"version"):
        from sweetheart import __version__
        print(MASTER_MODULE,__version__)
        exit()
    
    # set the relevant project for config
    if getattr(argv,"project",None):
        project = argv.project[0]

    elif getattr(argv,"service",None) == "jupyter":
        # intends starting jupyter service
        project = "jupyter"

    elif getattr(argv,"pylibs",None) \
    and [lib.startswith("jupyter") for lib in argv.pylibs]:
        # intends installing jupyter python libs
        project = "jupyter"

    else: project = MASTER_MODULE

    verbose("processed args:",argv,level=2)
    verbose("current project:",project)
    set_config(project=project)
    cli.apply_function()
