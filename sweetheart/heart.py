"""
heart.py is ... the heart of sweetheart!
provides services and utilities classes 
"""
import time
from sweetheart.globals import *
from sweetheart.bottle import SimpleTemplate

import uvicorn
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import Route,Mount,WebSocketRoute
from starlette.responses import HTMLResponse,FileResponse,JSONResponse

# try: import cherrypy
# except:
#     class cherrypy:
#         @staticmethod
#         def expose(*args):
#             """ set cherrypy.expose as a ghost method """
#             pass


class BaseService:

    # tracker for avoiding localhost conflicts
    ports_register = set()

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

        # ensure that self.port is not in use
        assert self.port not in BaseService.ports_register
        BaseService.ports_register.add(self.port)

    def switch_port_to(self,port_number:int):
        """ allow changing port number afterwards which can avoid conflicts
            typically testing all services and servers on localhost
            it will raise exception if port_number is already in use """

        self.port = self.uargs['port'] = port_number
        self.url = f"http://{self.host}:{self.port}"

        # ensure that port_number is not in use
        assert port_number not in BaseService.ports_register
        BaseService.ports_register.add(port_number)

    def run_local(self,service:bool=True):
        """ start and run the command attribute locally
            the 'command' attribute must be set previously """

        if service:
            sp.terminal(self.command,self.terminal)
            time.sleep(0.75)#FIXME: waiting time needed
        else:
            sp.shell(self.command)

    def cli_func(self,args):
        """ provided default function for command line interface """

        echo(f"run service:\n{self.command}")
        if getattr(args,"open_terminal",None): self.run_local(service=True)
        else: self.run_local(service=False)

    def set_websocket(self,dbname=None,encoding='json'):
        if not dbname: dbname = self.config['selected_DB']
        self.WS_dbname = dbname
        self.WS_route = f"/data/{dbname}"
        self.WS = get_WebSocketEndpoint(self,encoding)
        return self.WS_route, self.WS
    
    def on_receive(self,websocket,data):
        raise NotImplementedError

def get_WebSocketEndpoint(parent:object,encoding:str):
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
        self.command = f"rethinkdb --http-port 8180 -d {config.subproc['rethinkpath']}"
        if run_local: self.run_local(service=True)
    
    def connect(self,db:str=None):
        if hasattr(self,'conn'): self.conn.close()
        if db is None: db = self.config['selected_DB']
        self.conn = self.client.connect(self.host,self.port,db=db)

    def set_client(self):

        from rethinkdb import r

        self.client = r
        self.conn = r.connect(
            self.host,
            self.port,
            db=self.config['selected_DB'])

        self.reql = "self.client"
        return self.client,self.conn
        
    def table(self,data:dict) -> object:
        #NOTE: reset self.reql
        self.data = data
        self.reql = f"self.client.table('{data['table']}')"
        return self

    def filter(self,data:dict) -> object:
        self.reql += f".filter({data['filter']})"
        return self

    def insert(self,data:dict) -> object:
        self.reql += f".insert({data['insert']})"
        return self

    def update(self,data:dict) -> object:
        self.reql += f".update({data['update']})"
        return self

    def run(self,data:dict=None):
        # if given, data must be a dict providing a 'run' key
        if data: reql = self.reql + f".{data['run']}.run(self.conn)"
        else: reql = self.reql + ".run(self.conn)"
        self.reql = "self.client"
        result = eval(reql)
        #FIXME: handle result type and return
        if type(result) in [str,int,float,dict]: return result
        else: return list(result)

    async def fetch_endpoint(self,request):
        data = await request.json()
        return JSONResponse({
            'target': data['target'],
            'value': self.run(data) })
    
    def on_receive(self,websocket,data):
        """ used as the websocket receiver """
        
        if data.get('run') == 'update|insert':
            if list(self.table(data).filter(data).run()):
                return websocket.send_json(
                    self.table(data).filter(data).update(data).run() )
            else:
                values = {'insert': {
                    **json.loads(data['filter']),
                    **json.loads(data['update']) }}
                return websocket.send_json(
                    self.table(data).insert(values).run() )
        
    def __del__(self):
        # close last RethinkDB connection
        if hasattr(self,'conn'): self.conn.close()


# class MongoDB(BaseService):

#     def __init__(self,config:BaseConfig,run_local:bool=False):
#         """ set Mongo Database as a service """

#         # url auto set from config
#         super().__init__(config.database_host,config)
#         self.command = f"mongod --dbpath={config.subproc['mongopath']}"
#         if run_local: self.run_local(service=True)
        
#     def set_client(self):
#         """ set MongoDB client and select database given by config 
#             it provides default messages related to the database 
#             return pymongo.MongoClient, MongoClient.Database tuple """

#         from pymongo import MongoClient

#         self.client = MongoClient(host=self.host,port=self.port)
#         echo("available databases:",self.client.list_database_names()[3:])

#         self.database = self.client[self.config['selected_DB']]
#         echo(f"selected database:",self.config['selected_DB'])
#         echo("existing collections:",self.database.list_collection_names())

#         return self.client,self.database

#     def on_receive(self,websocket,data):

#         # collection.find_one(data['select'],{'_id':0})
#         # collection.update_one(data['select'],{'$set':data['values']})
#         # collection.insert_one(data['values'])
#         raise NotImplementedError


def HTMLTemplate(filename:str,**kwargs):
    """ provide a Starlette-like function for rendering templates
        including configuration data and some python magic stuff """

    os.chdir(BaseConfig._['working_dir'])

    if os.path.isfile(f"{BaseConfig._['templates_dir']}/{filename}"):
        # load template from filename if exists
        with open(f"{BaseConfig._['templates_dir']}/{filename}","r") as tpl:
            template = tpl.read()

    elif isinstance(filename,str):
        # alternatively test the given string as template
        template = filename

    else: raise TypeError

    for old,new in {
      # provide magic html rebase() syntax <!SWEETHEART html>
      f'<!{MASTER_MODULE.upper()} html>': \
          f'%rebase("{BaseConfig._["templates_base"]}")',

      # provide magic html facilities
      't-style': 'class', # switch for tailwindcss
      '<vue': '<div v-cloak id="VueApp"',
      '</vue>': '</div>',

      # provide magic <python></python> syntax
      '</python>': "</script>",
      '<python>': """<script type="text/python">
import json
from browser import window, document
console, r = window.console, window.r
def try_exec(code:str):
    try: exec(code)
    except: pass
def createVueApp(dict:dict):
    try_exec("r.onupdate = on_update")
    try_exec("r.onmessage = on_message")
    try_exec("window.vuecreated = vue_created")
    window.createVueApp(json.dumps(dict))\n""",

      }.items():
        template = template.replace(old,new)
    
    # render html from template and config
    template = SimpleTemplate(template)
    return HTMLResponse(template.render(
        __db__ = BaseConfig._['selected_DB'],
        **BaseConfig._['templates_settings'],
        **kwargs ))


class HttpServer(BaseService):

    def __init__(self,config:BaseConfig,set_database=False):
        """ set Starlette web-app as a service """
        
        # autoset url from config
        super().__init__(config.async_host,config)
        self.data = []

        # set default uvivorn server args
        self.uargs = {
            "host": self.host,
            "port": self.port,
            "log_level": "info" }

        if set_database == True: 
            # set RethinkDB enabling websocket
            run_local = self.config.is_rethinkdb_local
            self.database = RethinkDB(config,run_local)
            self.database.set_websocket()
            # explicit error message calling set_client()
            try: self.database.set_client()
            except: raise Exception("RethinkDB server not found")

    def mount(self,*args:Route):
        """ mount given Route(s) and set facilities from config """

        # ensure mount() call only once
        assert hasattr(self,'data')

        os.chdir(self.config['working_dir'])
        echo("mount webapp:",self.config['working_dir'])

        if not args:
            # switch port to 8181 and keep free 8000
            # allow looking documentation and testing webapp
            self.switch_port_to(8181)
            # auto route the default welcome message
            self.config.is_webapp_open = True
            self.data.append(Route("/",HTMLResponse(self.config.welcome())))

        elif len(args)==1 and isinstance(args[0],str):
            # route given html as a simple page for tests
            self.config.is_webapp_open = True
            self.data.append(Route("/",HTMLTemplate(args[0])))

        else: self.data.extend(args)

        if hasattr(self,'database'):
            # mount fetch endpoint and websocket
            self.data.extend([
                Route("/data", self.database.fetch_endpoint, methods=["POST"]),
                WebSocketRoute(self.database.WS_route, self.database.WS) ])

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

        self.command = \
            f"{config.python_bin} -m {config.subproc['.jupytercmd']} "+\
            f"--no-browser --notebook-dir={config['notebooks_dir']}"

        if run_local: self.run_local(service=True)

    def set_ipykernel(self):
        """ set ipython kernel for running JupyterLab """

        # get path,name of python env
        path,name = os.path.split(BaseConfig.python_env)
        sp.python("-m","ipykernel","install","--user",
            "--name",name,"--display-name",self.config.project,cwd=path)

    def set_password(self):
        """ required for JupyterLab initialization """
        sp.python("-m","jupyter","notebook","password","-y")
    

# class HttpStaticServer(BaseService):

#     def __init__(self,config:BaseConfig,run_local:bool=False):
#         """ set cherrypy as a service for serving static contents
#             should be used for improving server performances if needed """

#         # auto set url from config
#         super().__init__(config.static_host,config)
#         self.command =\
#             f"{config.python_bin} -m sweetheart.sweet cherrypy-server"
#         if run_local: self.run_local(service=True)

#     @cherrypy.expose
#     def default(self):
#         return """
#           <div style="text-align:center;">
#             <h1><br><br>I'm Ready<br><br></h1>
#             <h3>cherrypy server is running</h3>
#           </div>"""

#     def run_local(self,service):
#         """ run CherryPy for serving statics """
#         if service: sp.terminal(self.command,self.terminal)
#         else: cherrypy.quickstart(self,config=self.config.subproc['cherryconf'])
