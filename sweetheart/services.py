
from sweetheart import *
import time,configparser

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import Route,Mount,WebSocketRoute
from starlette.responses import HTMLResponse,FileResponse,JSONResponse,RedirectResponse


class BaseService:

    ports_register = set()
    system_dir = "/etc/systemd/system"

    allowed_sysd_options = {
        '[Unit]':
            ('Description','After','Before'),
        '[Service]':
            #NOTE: extented by default using set_service(**kwargs)
            ('ExecStart','ExecReload','Restart','Type','User'),
        '[Install]':
            ('WantedBy','RequiredBy') }

    def __init__(self,url:str,config:BaseConfig):
        """ 
        set basic features of Sweeheart service objects :

            - start server for both testing or production
            - set capabilities from cli, python script, juypter notebooks
            - ensure ports unicity for tests on localhost
            - allow setting websocket protocol in simple way
            - provide default API for exchanging data through http
            - provide a base config for running within systemd

        the given url should follow the http://host:port pattern
        sub-classes must set self.command attribute for running service
        """

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

    def switch_port_to(self,port_number:int):
        """ allow changing port number afterwards which can avoid conflicts
            typically testing all services and servers on localhost
            it will raise exception if port_number is already in use """

        self.port = self.uargs['port'] = port_number
        self.url = f"http://{self.host}:{self.port}"

        # ensure that port_number is not in use
        assert port_number not in BaseService.ports_register
        BaseService.ports_register.add(port_number)

    # def cli_func(self,args):
    #     """ this provides default function available from command line interface 
    #         e.g. called within cli.py as follow: cli.set_service("RethinkDB") """

    #     if getattr(args,"open_terminal",None):
    #         self.run_local(terminal=True)

    #     else: self.run_local(terminal=False)

    def set_service(self,Description:str=None,**kwargs):

        """ create and set config for new systemd service 
            kwargs keys must be supported service options
            
            [Unit]
              Description,After,Before
            [Service]
              ExecStart,ExecReload,Restart,Type,User,Group
            [Install]
              WantedBy,RequiredBy """

        # provide a ConfigParser for setting systemd
        self.sysd = configparser.ConfigParser()
        self.sysd.optionxform = str #! keep case of options 

        # set sections of systemd service file
        self.sysd.add_section('Unit')
        self.sysd.add_section('Service')
        self.sysd.add_section('Install')

        if Description:
            assert 'Description' not in kwargs
            self.sysd['Unit']['Description'] = Description

        # set given options within **kwargs
        for option,value in kwargs.items():

            section = "Service" #! default value
            for sctn in self.allowed_sysd_options:
                if option in self.allowed_sysd_options[sctn]:
                    section = sctn[1:-1]
                    break

            self.sysd[section][option] = value
        
        # output messsage
        verbose("set systemd service:",self.sysd,level=2)

    def enable_service(self,filename):
        """ write file and enable service within systemd
            it will provide default values when not given """

        # provide some flexibility with filename
        if filename.endswith(".service"): suffix = ""
        else: suffix = ".service"

        default_settings = {
            'Unit': {
                'Description': '[SWEETHEART] Service',
                'After': 'network.target' },
            'Service': {
                'Type': 'simple',
                'User': os.getuser(),
                'ExecStart': f'sh -c "{self.command}"' },
            'Install': {
                'WantedBy': 'default.target' }}
        
        # set the previous default settings if needed
        for section,optdic in default_settings.items():
            for option,value in optdic.items():
                if not self.sysd[section].get(option):
                    self.sysd[section][option] = value

        # write file and enable service in systemd
        tempfile = f"{self.config.root_path}/configuration/{filename}{suffix}"

        with open(tempfile,'w') as file_out:
            #! space_around_delimiters must be set at False
            self.sysd.write(file_out, space_around_delimiters=False )

        sp.sudo("cp",tempfile,self.system_dir)
        sp.sudo(f"systemctl enable {tempfile}")

    # def update_subproc_file(self,dict):
        #FIXME: add new service within subproc conf file
        # should become a class method provided by sp/BaseConfig/BaseService?
        self.config.subproc['systemd'].append(filename)

        with open(self.config.subproc_file,'r') as file_in:
            subproc_settings = json.load(file_in)
            subproc_settings.update({'systemd':self._.systemd})

        with open(self.config.subproc_file,'w') as file_out:
            json.dump(file_out)

    def run_local(self,service:str=None,terminal:bool=None):
        """ start and run the command attribute locally
            the 'command' attribute must be set previously """

        if service:
            sp.sudo("systemctl","reload-or-restart",service)
            time.sleep(2) #FIXME: waiting time needed with rethinkdb

        elif terminal:
            sp.terminal(self.command,self.terminal)

        else: sp.shell(self.command)

    @BETA
    def run_distant(self,service=None):
        """ start and run the command attribute through ssh
            the 'command' attribute must be set previously 
            #FIXME: at the time being, only for tests """

        if service:
            raise NotImplementedError

        else:
            assert self.protocol == "ssh"

            host = self.host
            key = self._.subproc['keypass']
            usr = self._.subproc['user'][key]
            pwd = sp.shell(f"{self._.HOME}/.local/bin/pass{key}")
            cmd = self.command

            run = lambda cmd: sp.terminal(cmd,self.terminal)
            run(f'export SSH_ASKPASS={pwd}; setsid ssh {usr}@{host} {cmd}')

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


class RethinkDB(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set RethinkDB as a service """

        #NOTE: url is auto set here from config
        super().__init__(config.database_host,config)
        assert self.protocol == 'rethinkdb'

        self.API = BaseAPI

        self.command = \
            f"rethinkdb --http-port 8180 -d {config['db_path']}"

        # self.set_unit(
        #     Description = "RethinkDB service made with Sweetheart",
        #     ExecStart = self.command,
        #     User = os.getuser() )

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
    
    @BETA
    async def fetch_endpoint(self,request):
        """ #FIXME: unsafe, only for tests """

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
        self._mounted_ = False
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
        assert self._mounted_ is False

        os.chdir(self.config['working_dir'])
        verbose("mount webapp:",self.config['working_dir'])

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
            # it assumes that args are Route objects
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
        self._mounted_ = True

        return self

    def pre_mount(self,*args:str):
        """ FIXME: only for tests """
        assert args
        self._mount_ = args

    def app(self,*args) -> Starlette:
        """ mount(*args) and return related Starlette object """

        args_are = lambda typ:\
            all([ isinstance(arg,typ) for arg in args ])

        if args_are(str):
            self.pre_mount(*args)
        
        if getattr(self,'_mount_',None):
            self.mount([ eval(str) for str in self._mount_ ])

        elif self._mounted_ is False:
            assert args_are((Route,Mount))
            self.mount(*args)
        
        return self.starlette

    def run_local(self,service:bool=False):
        """ run webapp within local Http server """

        if service:
            assert hasattr(self,'_mount_')
            mount = ',\n'.join(self._mount_)

            NginxUnit(self.config).load(f"""
'''
{ self.config.app_callable }
auto-generated using sweetheart.services.HttpServer
USER: { os.getuser() } DATE: { sp.stdout("date") }
'''

from sweetheart.services import *

config = set_config(
    # set here configuration of your sweetheart app
    { self.config.data })

{ self.config.app_callable } = HttpServer(config).app(
    # set here url routing of your sweetheart app
    { mount })""" )

        else:
            import uvicorn
            os.chdir(self.config['working_dir'])
            if not self._mounted_: self.mount()
            if self.config.is_webapp_open: webbrowser(self.url)
            uvicorn.run(self.starlette,**self.uargs)


class JupyterLab(BaseService):

    def __init__(self,config:BaseConfig,run_local:bool=False):
        """ set JupyterLab as a service """

        #NOTE: auto set url from config
        super().__init__(config.jupyter_host,config)

        self.command = \
            f"{config.python_bin} -m jupyterlab "+\
            f"--no-browser --notebook-dir={config['notebooks_dir']}"

        if run_local:
            self.run_local(service=True)

    def set_ipykernel(self,set_passwd:bool=False):
        """ set ipython kernel for running JupyterLab """

        # get path,name of python env
        path,name = os.path.split(BaseConfig.python_env)
        sp.python("-m","ipykernel","install","--user",
            "--name",name,"--display-name",self.config.project,cwd=path)

        if pwd:
            # set required password for JupyterLab
            sp.python("-m","jupyter","notebook","password","-y")


@BETA
class NginxUnit(UserDict):        

    def __init__(self,config:BaseConfig):
        self.config = self._ = config
        self.data =\
          {
            "listeners": {
                config.unit_listener: {
                    "pass": "routes"
                }
            },
            "routes": [{
                "action": {
                    "pass": "applications/starlette"
                }
            }],
            "applications": {
                "starlette": {
                    "type": f"python {config.python_version}",
                    "path": config.module_path,
                    "home": config.python_env,
                    "module": config.app_module,
                    "callable": config.app_callable,
                    "user": os.getuser()
                }
            }
          }

    def add_proxy(self,route,target):

        self["routes"].insert(0,{
                "match": {
                    "uri": f"/{route}/*"
                },
                "action": {
                    "proxy": target
                }
            })

    def load(self,py_module_content:str=None):

        host = self._.nginxunit_host
        socket = "/var/run/control.unit.sock"
        conf = f"{self._.root_path}/configuration/unit.json"

        with open(conf,'w') as file_out:
            json.dump(self.data, file_out)

        if isinstance(py_module_content,str):
            sp.overwrite_file(
                content= py_module_content,
                file= self.config.app_module+'.py',
                cwd= self.config.module_path )

        sp.sudo("curl","-X","PUT","-d",f"@{conf}","--unix-socket",socket,f"{host}/config/")
        sp.sudo("systemctl reload-or-restart unit")

    def stop(self):

        sp.sudo("systemctl stop unit")
        