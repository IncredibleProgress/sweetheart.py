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

    # select settings from subproc.json file
    with open(config.subproc_file) as infile:
        subproc_settings = json.load(infile)
    
    for key in ('pyenv','rustpath','codepath'):
        value = subproc_settings.get(key)
        if value: config.subproc[key] = value

    # set python env if given
    if config.subproc.get('pyenv'):
        BaseConfig.python_bin =\
            f"{config.subproc['pyenv']}/bin/python"


def webbrowser(url:str):
    """ start url within webbrowser set in config """

    try: select = config['webbrowser']
    except: select = None

    if select and config.subproc.get(select):
        sp.shell(config.subproc['select']+url)

    elif BaseConfig.WSL_DISTRO_NAME:
        sp.shell(config.subproc['msedge.exe']+url)

    else: sp.shell(config.subproc['firefox']+url)


def quickstart(*args):
    """ build and run webapp for the existing config """
    from sweetheart.heart import HttpServer,Database,Notebook

    try: 'config' in globals()
    except: set_config()

    # start jupyter lab server
    if config.is_jupyter_local:
        Notebook(config,run_local=True)

    # connect mongo database local server
    if config.is_mongodb_local:
        sp.mongo = Database(config,run_local=True)

    # build and start webapp
    webapp = HttpServer(config)
    webapp.mount(*args,open_with=webbrowser)
    webapp.run_local(service=False)


def sws(*args):
    """ SWeet Shell command line interface """

    try: 'config' in globals()
    except: raise Exception("Error, config is missing")

    # python_bin set only when needed
    if args[0].lower() in ['python','sweet','start']:
        config.ensure_python()

    switch = {
        'python': [f"{config.python_bin[:-7]}/ipython"],
        'mdbook': [f"{config.subproc['rustpath']}/mdbook"],
        'sweet': [f"{config.python_bin}","-m","sweetheart.sweet"],
        'start': [f"{config.python_bin}","-m","sweetheart.sweet","start"],
        } 
    
    args = list(args)
    arg0 = switch.get(args[0],[args[0]])
    try: sp.run(*arg0+args[1:])
    except: pass


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
        """ set a related function for the current parser or subparser """
        self.dict[self.cur].set_defaults(func=func)

    def set_parser(self):
        self.args = self.parser.parse_args()
        return self.args

    def quickstart(self,args):
        """ set quickstart call from cli """

        config.is_webapp = not args.server_only
        config.is_mongodb_local = not args.mongo_disabled
        config.is_jupyter_local = args.jupyter_lab
        quickstart()


if __name__ == "__main__":
    
    set_config()

    # build sweetheart command iine interface
    cli = CommandLineInterface()
    cli.set_function(lambda args:
        echo("type 'sws --help' for getting some help"))

    cli.opt("-v","--verbose",action="count",default=0,
        help="get additional messages about on-going process")

    cli.opt("-p",dest="project",nargs="?",const="sweetheart",
        help="set a project name different of sweetheart")

    cli.opt("-i","--init",action="store_true",
        help="launch init process for building new sweetheart project")


    # create subparser for the 'shell' command:
    cli.sub("shell",help="the SWeet Shell command line interface")
    cli.opt("subargs",nargs=cli.REMAINDER,help="remaining args processed by SWeet Shell")
    cli.set_function(lambda args: sws(*args.subargs))

    # create subparser for the 'start' command:
    cli.sub("start",help="start webapp with required services")
    cli.set_function(cli.quickstart)

    cli.opt("-x","--mongo-disabled",action="store_true",
        help="start without local Mongo Database server")

    cli.opt("-j","--jupyter-lab",action="store_true",
        help="start JupyterLab http server for enabling notebooks")

    cli.opt("-s","--server-only",action="store_true",
        help="start Http server without opening webbrowser")


    # execute command line arguments
    argv = cli.set_parser()
    BaseConfig.verbosity = argv.verbose

    if argv.project:
        set_config(project=argv.project)

    if argv.init is True:
        from sweetheart.install import init
        from sweetheart.heart import Notebook
        init(config)

        jupyter = Notebook(config)
        jupyter.set_ipykernel()
        jupyter.set_password()

    argv.func(argv)
