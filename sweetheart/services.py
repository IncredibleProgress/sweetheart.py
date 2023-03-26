
from sweetheart import *
import time,configparser
#from sweetheart.bottle import SimpleTemplate

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import Route,Mount,WebSocketRoute
from starlette.responses import HTMLResponse,FileResponse,JSONResponse,RedirectResponse


class BaseAPI(UserDict):

    model = {
        "info": {
            "title": "sweetAPI",
            "version": "0.1.0",
        },
        "header": {
            "service": str,
            "expected": "JSON",
            "database": None,
            "error": None,
        },
        "data": {} }

    def __init__(self,json):

        assert json.get('info')
        assert json.get('header')
        assert json['info']['title'] == self.model['info']['title']
        assert json['info']['version'] == self.model['info']['version']

        self.json = json
        self.data = json.get('data',{})
        self.service = json['header']['service']
        self.expected = json['header']['expected']
        self.response = dict(self.model)
    
    def ensure(self,dict):
        """ ensure service and data types consistency """

        assert dict['header']['service'] == self.service 
        self.response['header']['service'] = self.service
        assert dict['header'].get('database') == self.json['header'].get('database')
        self.response['header']['database'] = dict['header'].get('database')
        for k in dict['data']: assert isinstance(self[k],dict['data'][k])
        return self

    def eval(self,str,type_):

        if hasattr(self,'locals'):
            locals().update(self.locals)
        try:
            value = eval(str)
            assert isinstance(value,type_)
            return value
        except:
            self.response['header']['error'] = "data value error"
            return "!Err"

    def JSONResponse(self,data:dict):

        assert self.expected.upper() == "JSON"
        self.response['data'].update(data)
        return JSONResponse(self.response)


class BaseService:

    # ports tracker for avoiding localhost conflicts
    ports_register = set()

    def __init__(self,url:str,config:BaseConfig):
        """ set basic features of Sweeheart service objects :

             - start server for both testing or production
             - set capabilities from cli, python script, juypter notebooks
             - ensure ports unicity for tests on localhost
             - allow setting websocket protocol in simple way
             - provide default API for exchanging data through http
             - provide a base config for running within systemd

            the given url should follow the http://host:port pattern
            sub-classes must set self.command attribute for running service """

        self.API = BaseAPI
        self.config = self._ = config
        self.command = "echo Error, no command attribute given"

        if config.WSL_DISTRO_NAME: self.terminal = 'wsl'
        else: self.terminal = 'xterm'

        self.url = url
        url_split = url.split(":")
        self.protocol = url_split[0].lower()
        self.host = url_split[1].strip("/")
        self.port = int(url_split[2])

        #FIXME: ensure that self.port is not in use
        assert self.port not in BaseService.ports_register
        BaseService.ports_register.add(self.port)

        # provide a ConfigParser for setting systemd
        self.sysd = configparser.ConfigParser()

        # set usual sections of systemd service file
        self.sysd.add_section('Unit')
        self.sysd.add_section('Service')
        self.sysd.add_section('Install')

    def write_service_file(self,filename):
        """ write service file for setting systemd
            provide default value if not given """

        assert filename.endswith(".service")

        tempfile = f"{self.config.root_path}/configuration/{filename}"
        

        def ensure_default(section,param,default_value):
            assert section in "Unit|Service|Install"
            if self.sysd[section].get(param) is None:
                verbose("set systemd",f"[{section}]","default value:",param,"=",default_value)
                self.sysd[section][param] = default_value

        # [Unit] section
        ensure_default('Unit','Description',f'Sweetheart service')
        ensure_default('Unit','After',f'network.target')
        # [Service] section
        ensure_default('Service','ExecStart',self.command)
        ensure_default('Service','Type','simple')
        # [Install] section
        ensure_default('Install','WantedBy','default.target')

        # write and set service file for systemd
        self.sysd.write(tempfile)
        sp.shell(f"sudo cp {tempfile} /etc/systemd/system")

        # 

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
            time.sleep(2)#FIXME: waiting time needed
        else:
            sp.shell(self.command)

    def cli_func(self,args):
        """ this provides default function available from command line interface 
            e.g. called within cli.py as follow: cli.set_service("RethinkDB") """

        echo(f"run service: {self.command}")
        if getattr(args,"open_terminal",None): self.run_local(service=True)
        else: self.run_local(service=False)

    def set_websocket(self,dbname=None,set_encoding='json'):
        """ factory function for implementing starlette WebSocketEndpoint
            the parent class 'self' must provide an 'on_receive' method
            which is not implemented directly into BaseService """
        
        parent:BaseService = self
        if dbname is None: dbname=self.config['db_name']

        class WebSocket(WebSocketEndpoint):
            encoding = set_encoding
            service_config = {
                "encoding": encoding,
                "db_name": dbname,
                "route": f"/data/{dbname}",
                "receiver": parent.on_receive,
                }
            async def on_receive(self,websocket,data):
                receiver = self.service_config['receiver']
                await receiver(websocket,data)

        self.ws_config:dict = WebSocket.service_config
        self.WebSocketEndpoint:type = WebSocket
        verbose("new websocket endpoint: ",WebSocket.service_config['route'])
        return WebSocket.service_config['route'], WebSocket
    
    def on_receive(self,websocket,data):
        raise NotImplementedError


class RethinkDB(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set RethinkDB as a service """

        #NOTE: url is auto set here from config
        super().__init__(config.database_host,config)
        assert self.protocol == 'rethinkdb'

        self.command = \
            f"rethinkdb --http-port 8180 -d {config['db_path']}"

        # self.set_unit(
        #     Description = "RethinkDB service made with Sweetheart",
        #     ExecStart = self.command,
        #     User = BaseConfig.USER )

        if run_local: self.run_local(service=True)

    def set_client(self,dbname:str=None):

        # import rethinkdb only if needed
        from rethinkdb import r

        if dbname is None: dbname=self.config['db_name']
        self.conn = r.connect(self.host,self.port,db=dbname)
        self.client, self.dbname = r, dbname
        return self.client,self.conn

    def connect(self,dbname:str=None):

        if hasattr(self,'conn'): self.conn.close()
        if dbname is None: dbname=self.config['db_name']
        self.conn = self.client.connect(self.host,self.port,db=dbname)
        self.dbname = dbname
        return self.conn,self.dbname
        
    async def fetch_endpoint(self,request):
        """ #FIXME: unsecure, only for tests """

        api = self.API(await request.json()).ensure({
            "header": { 
                "service": "fetch|JSON|<ELEMENT>",
                "database": self.dbname },
            "data": {
                "target": str,
                "reql": str } })

        api.locals = dict(r=self.client,conn=self.conn)
        return api.JSONResponse({
            "target": api['target'],
            "value": api.eval(f"r.{api['reql']}.run(conn)",str) })
    
    def on_receive(self,websocket,data):
        """ provide a RethinkDB websocket receiver 
            allow update or insert data into a table """

        print(type(data))
        api = self.API(json.loads(data)).ensure({
            "header": { 
                "service": "ws|ReQL.UPDATE|<LOG>",
                "database": self.dbname },
            "data": {
                "table": str,
                "filter": dict,
                "update": dict } })
        
        _table = f"table({api['table']})"
        _filter = f"filter({api['filter']})"
        _update = f"update({api['update']})"

        if eval(f"self.client.{_table}.{_filter}.run(self.conn)"): 
            # Update data within database
            reql = f"r.{_table}.{_filter}.{_update}.run(conn)"
        else:
            # Insert data within database
            values = { **api['filter'], **api['update'] }
            reql = f"r.{_table}.insert({values}).run(conn)"
        
        api.locals = dict(r=self.client,conn=self.conn)
        api.update({ "log": api.eval(reql) })
        return websocket.send_json(api.response)

    def __del__(self):
        # close last RethinkDB connection
        if hasattr(self,'conn'): self.conn.close()


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
            # explicit error message calling set_client()
            try: self.database.set_client()
            except: raise Exception("Error, RethinkDB server not found")

    def mount(self,*args:Route) -> BaseService:
        """ mount given Route(s) and set facilities from config """

        # ensure mount() call only once
        assert hasattr(self,'data')

        os.chdir(self.config['working_dir'])
        echo("mount webapp:",self.config['working_dir'])

        if not args:

            WelcomeMessage = lambda: HTMLResponse(f"""
                <div style="text-align:center;font-size:1.1em;">
                    <h1><br><br>Welcome !<br><br></h1>
                    <h2>sweetheart</h2>
                    <p>a supercharged heart for the non-expert hands</p>
                    <p>which will give you coding full power at the light speed</p>
                    <p><a href="/documentation/index.html">
                        Get Started Now!</a></p>
                    <p><br>or code immediately using 
                        <a href="{BaseConfig.jupyter_host}">JupyterLab</a></p>
                    <p><br><br><em>this message appears because there
                    was nothing else to render here</em></p>
                </div> """)

            # switch port to 8181 and keep free 8000
            # allow looking documentation and testing webapp
            self.switch_port_to(8181)
            # auto route the default welcome 
            self.data.append( Route("/",WelcomeMessage()) )

        elif len(args)==1 and isinstance(args[0],str):
            # route given template as a simple page for tests
            self.config.is_webapp_open = True
            self.data.append( Route("/",HTMLTemplate(args[0])) )

        else:
            # assumes that args are Route objects
            self.data.extend(args)

        if hasattr(self,'database'):
            # set websocket if not already done
            if not hasattr(self.database,'WebSocketEndpoint'):
                self.database.set_websocket()
            # mount fetch and websocket endpoints
            self.data.extend([
                Route("/data",self.database.fetch_endpoint,methods=["POST"]),
                WebSocketRoute(self.database.ws_config['route'],self.database.WebSocketEndpoint) ])

        # mount static files given within config
        self.data.extend([Route(relpath,FileResponse(srcpath))\
            for relpath,srcpath in self.config["static_files"].items()])

        # mount static directories given within config
        self.data.extend([Mount(relpath,StaticFiles(directory=srcpath))\
            for relpath,srcpath in self.config["static_dirs"].items()])

        # set the webapp Starlette object
        self.starlette = Starlette(routes=self.data)
        del self.data# new setting forbidden

        return self

    def app(self,*args:Route) -> Starlette:
        """ mount(*args) and return related Starlette object """
        self.mount(*args)
        return self.starlette

    def run_local(self,service:bool=False):
        """ run webapp within local Http server """

        if service:
            #FIXME: deprecated
            os.chdir(self.config['working_dir'])
            sp.python(
                "-m","gunicorn","main:app",
                "--workers",4,
                "--worker-class","uvicorn.workers.UvicornWorker",
                "--bind","0.0.0.0:80",
                cwd= self.config._['module_path'])
        else:
            import uvicorn
            os.chdir(self.config['working_dir'])
            if hasattr(self,"data"): self.mount()
            if self.config.is_webapp_open: webbrowser(self.url)
            uvicorn.run(self.starlette,**self.uargs)


class JupyterLab(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set JupyterLab as a service """

        # auto set url from config
        super().__init__(config.jupyter_host,config)

        self.command = \
            f"{config.python_bin} -m jupyterlab "+\
            f"--no-browser --notebook-dir={config['notebooks_dir']}"

        self.set_unit(
            Description = "JupyterLab service made with Sweetheart",
            ExecStart = self.command,
            User = BaseConfig.USER )

        if run_local: self.run_local(service=True)

    def set_ipykernel(self,pwd:bool=False):
        """ set ipython kernel for running JupyterLab """

        # get path,name of python env
        path,name = os.path.split(BaseConfig.python_env)
        sp.python("-m","ipykernel","install","--user",
            "--name",name,"--display-name",self.config.project,cwd=path)

        if pwd:
            # set required password for JupyterLab
            sp.python("-m","jupyter","notebook","password","-y")



class NginxUnit(UserDict):
    #FIXME: to implement

    def __init__(self,config:BaseConfig):

        self._ = config
        self.data =\
          {
            "listeners": {
                self._.unit_listener: {
                    "pass": "routes"
                }
            },
            "routes": [
                {
                    "match": {
                        "uri": "/jupyter/*"
                    },
                    "action": {
                        "proxy": config.jupyter_host
                    }
                },
                {
                    "action": {
                        "pass": "applications/starlette"
                    }
                }
            ],
            "applications": {
                "starlette": {
                    "type": f"python {config.python_version}",
                    "path": config.module_path,
                    "home": config.python_env,
                    "module": config.app_module,
                    "callable": config.app_callable,
                    "user": "ubuntu"
                }
            }
          }

    def put_config(self):

        host = self._.nginxunit_host
        conf = f"{self._.root_path}/configuration/unit.json"

        with open(conf,'w') as file_out:
            json.dump(self.data, file_out)

        sp.shell("sudo","curl","-X","PUT","-d",f"@{conf}",
            "--unix-socket","/var/run/control.unit.sock",f"{host}/config/")
        
        sp.shell("sudo","systemctl","restart","unit")

    def stop(self):
        sp.shell("sudo","systemctl","stop","unit")
        