"""
heart.py is ... the heart of sweetheart !
it provides services and facilities classes 
"""
from sweetheart.globals import *

from starlette.applications import Starlette
from starlette.responses import HTMLResponse,FileResponse,RedirectResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles


class BaseService:

    def __init__(self,url:str,config:BaseConfig) -> None:
        """ set basic features of sweeheart service objects
            the given url should follow http://host:port pattern
            the child class must set self.command attribute """

        self.config = config
        self.command = "echo Error, no command attribute given"

        if config.WSL_DISTRO_NAME: self.terminal = 'wsl'
        else: self.terminal = 'xterm'

        self.url = url
        self.host = url.split(":")[1].strip("/")
        self.port = int(url.split(":")[2])

    def run_local(self,service:bool=True):
        """ start and run the command attribute locally
            self.command must be set previously """

        if service:
            # run service locally opening new shell
            sp.terminal(self.command,self.terminal)
        else:
            # run service locally within current shell
            sp.shell(self.command)

    def cli_func(self,args):
        """ provided function for command line interface """
        raise NotImplementedError


class Database(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set Mongo Database as a service """

        #NOTE: auto set url from config
        super().__init__(config.database_host,config)
        self.command = config.subproc['mongodb']

        if run_local: self.run_local(service=True)
        
    def set_client(self):
        """ set MongoDB client and select database given by config 
            it provides default messages related to the database 
            return pymongo.MongoClient, MongoClient.Database tuple """

        from pymongo import MongoClient

        self.client = MongoClient(host=self.host,port=self.port)
        echo("available mongo databases:",
            self.client.list_database_names())

        self.database = self.client[self.config['db_select']]
        echo(f"selected database:",self.config['db_select'],
            "\nexisting mongo collections:",
            self.database.list_collection_names())

        return self.client,self.database
    
    def cli_func(self,args):
        """ provided function for command line interface """
        self.run_local(service=False)


class HttpServer(BaseService):

    def __init__(self,config:BaseConfig) -> None:
        """ set Starlette web-app as a service """
        
        #NOTE: self.command not set here
        #NOTE: url is auto set here from config
        super().__init__(config.async_host,config)
        self.data = []

        # set default uvivorn server args
        self.uargs = {
            "host": self.host,
            "port": self.port,
            "log_level": "info" }

    def mount(self,*args:Route,open_with:callable=None):
        """ mount given Route(s) and set facilities from config
            open_with allows setting a function for opening self.url """

        assert hasattr(self,'data')
        os.chdir(self.config['working_dir'])
        echo("mount webapp:",self.config['working_dir'])

        if not args:
            # set a welcome message
            self.data.append(
                Route("/",HTMLResponse(self.config.welcome)))
        else:
            self.data.extend(args)

        # mount static files given within config
        self.data.extend([Route(relpath,FileResponse(srcpath))\
            for relpath,srcpath in self.config["static_files"].items()])

        # mount static directories given within config
        self.data.extend([Mount(relpath,StaticFiles(directory=srcpath))\
            for relpath,srcpath in self.config["static_dirs"].items()])

        # set the webapp Starlette object
        self.app = Starlette(routes=self.data)
        del self.data# new setting forbidden

        # open url when relevant
        if self.config.is_webapp_open and open_with:
            open_with(self.url)

    def run_local(self,service:bool):
        """ run web-app within local Http server """

        if service == False:
            import uvicorn
            #NOTE: current working dir should not be changed
            assert os.getcwd() == self.config['working_dir']
            uvicorn.run(self.app,**self.uargs)
        else:
            # run self.command if given
            super().run_local(service)


class Notebook(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False) -> None:
        """ set JupyterLab as a service """

        #NOTE: auto set url from config
        super().__init__(config.jupyter_host,config)

        self.config.ensure_python()
        self.python_env = config.python_bin[:-7]

        self.command = f"{config.python_bin} -m jupyterlab \
            --no-browser --notebook-dir={config['notebooks_dir']}"

        if run_local: self.run_local(service=True)

    def set_ipykernel(self):
        """ set ipython kernel for running JupyterLab """

        # get path,name of python env
        path,name = os.path.split(self.python_env)

        os.chdir(path)
        print("\n[WARNING] Set a password for JupyterLab server is required")
        sp.python("-m","ipykernel","install","--user",f"--name={name}")

    def set_password(self):
        """ required for JupyterLab initialization """
        sp.python("-m","jupyter","notebook","password","-y")
    
    def cli_func(self, args):
        """ JupyterLab command line function """
        self.run_local(service=True)
    