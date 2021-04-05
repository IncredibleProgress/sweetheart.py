"""
sweet.py is the multi-purpose controller of sweetheart
it provides cli, install process, sandbox and services
"""
from sweetheart.globals import *


def set_config(values:dict={},project:str="sweetheart",file:str=None):
    """ set or reset sweetheart configuration 
        allow working with differents projects and configs """

    global config
    config = BaseConfig(project)
    if file: config.config_file = file

    try: 
        # update config from given json file
        with open(config.config_file) as infile:
            config.update(json.load(infile))
            verbose("config file:",config.config_file)
    except: pass

    # allow altered config
    config.update(values)

    try: 
        # get subproc settings from given json file
        with open(config.subproc_file) as infile:
            subproc_settings = json.load(infile)
            verbose("subproc file:",config.subproc_file)

        # fix updatable subproc settings here
        for key in ('pyenv','rustpath','codepath'):

            value = subproc_settings.get(key)
            if key == 'pyenv': 
                BaseConfig.python_env = value
                BaseConfig.python_bin = f"{value}/bin/python"
            elif value:
                config.subproc[key] = value
    except: pass

    # ensure python/poetry subprocess
    BaseConfig.cwd = config.subproc['codepath']
    if hasattr(BaseConfig,'python_env') is False:
        sp.set_python_env()


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

    try: assert 'config' in globals()
    except: set_config(project="sweetheart")

    # start Jupyterlab server
    if config.is_jupyter_local:
        Notebook(config,run_local=True)

    # connect mongo database server
    if config.is_mongodb_local:
        sp.mongo = Database(config,run_local=True)

    # build and start webapp
    webapp = HttpServer(config)
    webapp.mount(*args,open_with=webbrowser)
    webapp.run_local(service=False)


def sws(*args):
    """ SWeet Shell command line interface """

    try: assert 'config' in globals()
    except: raise Exception("Error, config is missing")

    cf,sb = config, config.subproc
    sw = [config.python_bin,"-m","sweetheart.sweet"]
    vv,py,po = config.python_env,config.python_bin,config.poetry_bin

    switch = {
        'python': [f"{vv}/bin/ipython",*args[1:]],
        'poetry': [config.poetry_bin,*args[1:]],
        'mdbook': [f"{sb['rustpath']}/mdbook",*args[1:]],
        'sweet': [py,"-m","sweetheart.sweet",*args[1:]],
        'start': [py,"-m","sweetheart.sweet","start",*args[1:]],
        'jupyter': [py,"-m","jupyter",*args[1:]],
        }

    if args[0]=='poetry': cwd= BaseConfig.cwd
    elif args[0]=='mdbook': cwd= f"{cf.root_path}/documentation"
    else: cwd= config.PWD

    try: sp.run(*switch.get(args[0],args),cwd=cwd)
    except: echo("sws has been interrupted")


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

    # build sweetheart command iine interface
    cli = CommandLineInterface()
    cli.set_function(lambda args:
        echo("type 'sws help' for getting some help",blank=True))

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
    else:
        set_config(project="sweetheart")

    if argv.init is True:
        
        from sweetheart.install import init
        init(config)

        from sweetheart.heart import Notebook
        echo("set JupyerLab ipkernel and required password",blank=True)
        jupyter = Notebook(config)
        jupyter.set_ipykernel()
        jupyter.set_password()

    argv.func(argv)
