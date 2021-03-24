"""
heart.py is ... the heart of sweetheart !
it provides base usefulle servers and services
"""
import os,sys
from collections import UserList

from sweetheart.globals import *
from sweetheart.subproc import BaseService,sp

from starlette.applications import Starlette
from starlette.responses import HTMLResponse,FileResponse,RedirectResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles


def webbrowser(url:str,config:BaseConfig=None):

    try: select = config['webbrowser']
    except: select = None

    if select and config.subproc.get(select):
        sp.shell(config.subproc['select'])

    elif os.environ.get('WSL_DISTRO_NAME'):
        sp.shell(config.subproc['msedge.exe'])

    else: sp.shell(config.subproc['firefox'])


class Database(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set Mongo Database as a service """

        #NOTE: auto set url from config
        super().__init__(config.database_host,config)
        self.command = config.subproc['mongodb']

        if run_local: self.run_local(service=True)
        
    def set_client(self):
        """ set MongoDB client and select database given by config 
            it provides default messages related to the database """

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
        """ set command ligne function """
        self.run_local(service=False)


class Webapp(BaseService,UserList):

    def __init__(self,config:BaseConfig) -> None:
        """ set a Starlette webapp as a service """

        #NOTE: auto set url from config
        super(BaseService,self).__init__(config.async_host,config)
        self.command = "sws run-webapp"

        # set default uvivorn server args
        self.uargs = {
            "host": self.host,
            "port": self.port,
            "log_level": "info" }

    def mount(self,*args:Route):

        # mount() can be called only once
        assert not hasattr(self,"app")

        if not args:
            # set a welcome message
            self.data.append(
                Route("/",HTMLResponse(self.config.welcome)) )
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

    def run_local(self,service:bool):
        """ run webapp on a local async server """
        if service == False:
            import uvicorn
            uvicorn.run(self.app,*self.uargs)
        else:
            super(BaseService,self).run_local(service)

    def cli_func(self,args):
        """ set command ligne function """
        self.run_local(service=False)

    def quickstart(self,*args:Route):

        # connect mongo database local server
        if self.config.is_mongodb_local:
            mongod = Database(self.config,run_local=True)
            self.mongoclient,self.database = mongod.set_client()

        # connect mdbook local server
        # connect cherrypy local server
        # start webbrowser
        webbrowser(self.url,self.config)

        # start webapp
        os.chdir(self.config['working_dir'])
        self.mount(*args)
        self.run_local(service=False)
