"""
heart.py is ... the heart of sweetheart !
it provides services and facilities classes 
"""
from sweetheart.globals import *
from sweetheart.bottle import SimpleTemplate

# patch running within JupyterLab
import nest_asyncio
nest_asyncio.apply()

import uvicorn
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.responses import HTMLResponse,FileResponse,RedirectResponse

try: import cherrypy
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
        url_split = url.split(":")
        self.protocol = url_split[0].lower()
        self.host = url_split[1].strip("/")
        self.port = int(url_split[2])

    def run_local(self,service:bool=True):
        """ start and run the command attribute locally
            the 'command' attribute must be set previously """

        if service: sp.terminal(self.command,self.terminal)
        else: sp.shell(self.command)

    def cli_func(self,args):
        """ provided default function for command line interface """

        echo(f"run service:\n{self.command}")
        if getattr(args,"open_terminal",None): self.run_local(service=True)
        else: self.run_local(service=False)

    def set_websocket(self,encoding='json'):
        self.WS = get_websocket(self,encoding)
        return self.WS


def get_websocket(parent:object,encoding:str):
    """ factory function for implementing WebSocketEndpoint 
        the object 'parent' must provide an 'on_receive' method """

    class WebSocket(WebSocketEndpoint):
        async def on_receive(self,websocket,data):
            await parent.on_receive(websocket,data)

    WebSocket.encoding = encoding
    return WebSocket


class RethinkDB(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set RethinkDB as a service """

        #NOTE: url is auto set here from config
        super().__init__(config.database_host,config)
        assert self.protocol == 'rethinkdb'

        self.command = f"rethinkdb -d {config.subproc['rethinkpath']}"
        if run_local: self.run_local(service=True)
    
    def connect(self,db:str=None):

        if hasattr(self,'conn'): self.conn.close()
        if db is None: db = self.config['selected_DB']
        self.conn = self.client.connect(self.host,self.port,db=db)

    def set_client(self):

        from rethinkdb import r
        self.client = r
        self.conn = r.connect(self.host,self.port,db=self.config['selected_DB'])
        return self.client,self.conn
    
    def on_receive(self,websocket,data):
        
        reql = eval(f"self.client.table('{data['table']}').filter({data['filter']}).run(self.conn)")

        return websocket.send_json({
            'grid_id': data['filter']['grid_id'],
            'select': 'test',
            'reql': list(reql) })

    def __del__(self):

        if hasattr(self,'conn'): 
            self.conn.close()
            verbose("the last RethinkDB connection has been closed")


class MongoDB(BaseService):

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
        echo("available databases:",self.client.list_database_names()[3:])

        self.database = self.client[self.config['selected_DB']]
        echo(f"selected database:",self.config['selected_DB'])
        echo("existing collections:",self.database.list_collection_names())

        return self.client,self.database

    def on_receive(self,websocket,data):

        # collection.find_one(data['select'],{'_id':0})
        # collection.update_one(data['select'],{'$set':data['values']})
        # collection.insert_one(data['values'])
        raise NotImplementedError


def HTMLTemplate(filename:str,**kwargs):
    """ set given template and return the rendering 
        including some configuration and python stuff """

    os.chdir(BaseConfig._['working_dir'])

    with open(f"{BaseConfig._['templates_dir']}/{filename}","r") as tpl:
        template = tpl.read()
        for old,new in {
        '<!SWEETHEART html>': r'%rebase("HTML")',
        '<script python>': "\n".join((
            '<script type="text/python">\n',
            'import json',
            'from browser import window, document\n',
            'console, websocket = window.console, window.websocket',
            'createVueApp= lambda dict: window.createVueApp(json.dumps(dict))',
            'websocket.send_json= lambda dict: websocket.send(json.dumps(dict))',
            ))
        }.items(): template = template.replace(old,new)
        template = SimpleTemplate(template)

    return HTMLResponse(template.render(
        **BaseConfig._['templates_settings'],
        **kwargs ))


class HttpServer(BaseService):

    def __init__(self,config:BaseConfig,set_database:bool=False):
        """ set Starlette web-app as a service """
        
        # auto set url from config
        super().__init__(config.async_host,config)
        self.data = []

        # set default uvivorn server args
        self.uargs = {
            "host": self.host,
            "port": self.port,
            "log_level": "info" }

        if set_database: 
            self.database = RethinkDB(config)
            self.database.set_websocket()
            self.database.set_client()

    def mount(self,*args:Route):
        """ mount given Route(s) and set facilities from config """

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

        # mount websocket
        if hasattr(self,'database'):
            self.data.append(WebSocketRoute("/data",self.database.WS))

        # mount static files given within config
        self.data.extend([Route(relpath,FileResponse(srcpath))\
            for relpath,srcpath in self.config["static_files"].items()])

        # mount static directories given within config
        self.data.extend([Mount(relpath,StaticFiles(directory=srcpath))\
            for relpath,srcpath in self.config["static_dirs"].items()])

        # set the webapp Starlette object
        self.app = Starlette(routes=self.data)
        del self.data# new setting forbidden

        return self

    def run_local(self,service:bool=False):
        """ run webapp within local Http server """

        if self.config.is_webapp_open: webbrowser(self.url)

        if service:
            raise NotImplementedError
        else:
            os.chdir(self.config['working_dir'])
            uvicorn.run(self.app,**self.uargs)


class JupyterLab(BaseService):

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
    

class HttpStaticServer(BaseService):

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
        else: cherrypy.quickstart(self,config=self.config.subproc['cherryconf'])
