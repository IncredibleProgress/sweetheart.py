"""
heart.py is ... the heart of sweetheart !
it provides services and facilities classes 
"""
from sweetheart.globals import *

# patch running within JupyterLab
import nest_asyncio
nest_asyncio.apply()

import uvicorn
from bottle import template

from starlette.applications import Starlette
from starlette.responses import HTMLResponse,FileResponse,RedirectResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

try:
    import cherrypy
except:
    class cherrypy:
        @staticmethod
        def expose(*args):
            """ set cherrypy.expose as a ghost method """
            pass


class BaseService:

    def __init__(self,url:str,config:BaseConfig):
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

        if service: sp.terminal(self.command,self.terminal)
        else: sp.shell(self.command)

    def cli_func(self,args):
        """ provided default function for command line interface """

        echo(f"run service:\n{self.command}")
        if getattr(args,"open_terminal",None): self.run_local(service=True)
        else: self.run_local(service=False)


class Database(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set Mongo Database as a service """

        # url auto set from config
        super().__init__(config.database_host,config)
        self.command = f"mongod --dbpath={config.subproc['mongopath']}"

        if run_local: self.run_local(service=True)
        
    def set_client(self):
        """ set MongoDB client and select database given by config 
            it provides default messages related to the database 
            return pymongo.MongoClient, MongoClient.Database tuple """

        from pymongo import MongoClient

        self.client = MongoClient(host=self.host,port=self.port)
        echo("available mongo databases:",
            self.client.list_database_names())

        self.database = self.client[self.config['selected_DB']]
        echo(f"selected database:",self.config['selected_DB'],
            "\nexisting mongo collections:",
            self.database.list_collection_names())

        return self.client,self.database


class HttpServer(BaseService):

    def __init__(self,config:BaseConfig):
        """ set Starlette web-app as a service """
        
        # auto set url from config
        super().__init__(config.async_host,config)
        self.data = []

        # set default uvivorn server args
        self.uargs = {
            "host": self.host,
            "port": self.port,
            "log_level": "info" }

    def HTMLTemplate(self,filename:str,**kwargs):
        os.chdir(f"{self.config['working_dir']}")
        return HTMLResponse(template(
            f"{self.config['templates_dir']}/{filename}",
            **self.config['templates_settings'],
            **kwargs ))

    def mount(self,*args:Route,open_with:callable=None):
        """ mount given Route(s) and set facilities from config
            open_with allows setting a function for opening self.url """

        assert hasattr(self,'data')
        os.chdir(self.config['working_dir'])
        echo("mount webapp:",self.config['working_dir'])

        if not args:
            # change port to 8181 (keep free 8000)
            self.port = self.uargs['port'] = 8181
            self.url = f"http://{self.host}:{self.port}"
            # route welcome message
            self.data.append(Route("/",HTMLResponse(self.config.welcome())))
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

    def run_local(self,service:bool=False):
        """ run webapp within local Http server """

        if service:
            raise NotImplementedError
        else:
            os.chdir(self.config['working_dir'])
            uvicorn.run(self.app,**self.uargs)


class Notebook(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set JupyterLab as a service """

        # auto set url from config
        super().__init__(config.jupyter_host,config)

        self.command = f"{config.python_bin} -m jupyterlab \
            --no-browser --notebook-dir={config['notebooks_dir']}"

        if run_local: self.run_local(service=True)

    def set_ipykernel(self):
        """ set ipython kernel for running JupyterLab """

        # get path,name of python env
        path,name = os.path.split(BaseConfig.python_env)
        sp.python("-m","ipykernel","install","--user",f"--name={name}",cwd=path)

    def set_password(self):
        """ required for JupyterLab initialization """
        sp.python("-m","jupyter","notebook","password","-y")
    

class StaticServer(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set cherrypy as a service for serving static contents
            should be used for improving server performances if needed """

        # auto set url from config
        super().__init__(config.static_host,config)
        
        self.command =\
            f"{config.python_bin} -m sweetheart.sweet cherrypy-server"

        if run_local: self.run_local(service=True)

    @cherrypy.expose
    def default(self):
        return """
          <div style="text-align:center;">
            <h1><br><br>I'm Ready<br><br></h1>
            <h3>cherrypy server is running</h3>
          </div>"""

    def run_local(self,service):
        """ run CherryPy for serving statics """
        if service: sp.terminal(self.command,self.terminal)
        else: cherrypy.quickstart(self,config=self.config.subproc['cherrypy'])
