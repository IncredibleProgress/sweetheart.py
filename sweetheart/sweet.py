"""
sweet.py is the multi-purpose controller of sweetheart
it provides cli, install process, sandbox and services
"""
from sweetheart.globals import *


def set_config(values:dict={},project:str="sweetheart"):
    """ set or reset sweetheart configuration """

    global config
    config = BaseConfig(project)
    config.update(values)


def webbrowser(url:str):
    """ start url within webbrowser set in config """

    try: select = config['webbrowser']
    except: select = None

    if select and config.subproc.get(select):
        sp.shell(config.subproc['select'])

    elif BaseConfig.WSL_DISTRO_NAME:
        sp.shell(config.subproc['msedge.exe'])

    else: sp.shell(config.subproc['firefox'])


def quickstart(*args):
    """ build and run webapp for the existing config """

    from sweetheart.heart import Database,Webapp
    try: 'config' in globals()
    except: raise Exception("Error, config is missing")

    # connect mongo database local server
    if config.is_mongodb_local:
        sp.mongo = Database(config,run_local=True)

    # connect mdbook local server
    # connect cherrypy local server

    # set webapp
    webapp = Webapp(config)
    webapp.mount(*args)
    # start webapp
    if config.is_webapp: webbrowser(webapp.url)
    webapp.run_local(service=False)


def sws(self,*args):
    """ sweet shell command call """
    print("args:",args)
    print("type 'sws --help' or 'sws -h' for getting some help")


if __name__ == "__main__":

    set_config()
    sp.set_python_env(path=config.subproc['codepath'])

else: sp.exit()


class CommandLineInterface:

    def __init__(self) -> None:
        """ build python Command Line Interface with ease
            it uses argparse but provides better look and feel """

        # provide default parsers tools
        import argparse
        self.parser= argparse.ArgumentParser()
        self.subparser= self.parser.add_subparsers()
        self.dict= { "_": self.parser }
        self.cur= "_"
    
    def opt(self,*args,**kwargs):
        self.dict[self.cur].add_argument(*args,**kwargs)

    def sub(self,*args,**kwargs):
        self.cur = args[0]
        self.dict[args[0]] = self.subparser.add_parser(*args,**kwargs)
    
    def set_function(self,func):
        """ set a related function for the current parser or subparser """
        self.dict[self.cur].set_defaults(func=func)

    def set_parser(self):
        self.args = self.parser.parse_args()
        return self.args

    def quickstart(self,*args):
        """ quickstart call from cli """
        quickstart()


# build sweetheart command iine interface
cli = CommandLineInterface()
cli.set_function(sws)

cli.opt("-v","--verbose",action="count",
    help="get additional messages about on-going process")

cli.opt("-p",dest="project",action="store",nargs="?",const="sweetheart",
    help="set a project name different of sweetheart")

cli.opt("-i","--init",action="store_true",
    help="launch init process for building new sweetheart project")

# create the subparser for the "run-webapp" command:
cli.sub("start",help="start webapp with required services")
cli.set_function(cli.quickstart)


argv = cli.set_parser()
if argv.init is True:

    from sweetheart.install import init
    init(config)

argv.func(argv)
