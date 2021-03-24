"""
sweet.py is the multi-purpose controller of sweetheart
it provides cli, install process, sandbox and services
"""
import os,sys
from sweetheart.globals import *


def set_config(values:dict={},project:str="sweetheart"):
    """ set or reset sweetheart configuration """

    global config
    config = BaseConfig(project)
    config.update(values)


if __name__ == "__main__": set_config()
else: sys.exit()


#############################################################################
 ########## COMMAND LINE INTERFACE ###########################################
  #############################################################################

import argparse
from sweetheart.heart import Webapp


class CommandLineInterface:

    def __init__(self) -> None:
        """ Build python Command Line Interface with ease.
            It uses argparse but provides better look and feel. """

        # provide default parsers tools
        self.parser= argparse.ArgumentParser()
        self.subparser= self.parser.add_subparsers()
        self.dict= { "_": self.parser }
        self.cur= "_"

        # set help message
        self.call(lambda args:\
            print("use the '--help' or '-h' option for getting some help"))
    
    def opt(self,*args,**kwargs):
        self.dict[self.cur].add_argument(*args,**kwargs)

    def sub(self,*args,**kwargs):
        self.cur = args[0]
        self.dict[args[0]] = self.subparser.add_parser(*args,**kwargs)
    
    def call(self,func):
        """ set a related function for the current parser or subparser """
        self.dict[self.cur].set_defaults(func=func)

    def set_parser(self):
        self.args = self.parser.parse_args()
        return self.args


# build sweetheart command iine interface
cli = CommandLineInterface()

cli.opt("-v","--verbose",action="count",
    help="get additional messages about on-going process")

cli.opt("-p",dest="project",action="store",nargs="?",const="sweetheart",
    help="set a project name different of sweetheart")

cli.opt("-i","--init",action="store_true",
    help="launch init process for building new sweetheart project")

# create the subparser for the "run-webapp" command:
cli.sub("run-webapp",help="run webapp with required services")
cli.call(Webapp(config).cli_func)


cli.set_parser()
if cli.args.init is True:

    from sweetheart import subproc
    subproc.init(set_config(project=cli.args.project))
