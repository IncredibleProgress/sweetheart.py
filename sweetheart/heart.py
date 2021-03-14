"""
heart.py is ... the heart of sweetheart !
it provides base class for servers and services
"""
import os,subprocess
from sweetheart.globals import *


#############################################################################
 ########## SERVICES #########################################################
  #############################################################################

class BaseService:
    """
    provides common basis and signature for servers facilities 
     - attr.:
        url host port
     - methodes:
        service() subproc() cmd() run_local() commandLine()
    """

    def __init__(self,host:str="",port:int="",url:str=""):
        
        if url:
            assert url.startswith("http")
            self.url = url
            self.host = url.split(":")[1].strip("/")
            self.port = int(url.split(":")[2])

        elif host and port:
            self.url = f"http://{host}:{port}"
            self.host = host
            self.port = port

        else: raise AttributeError

    def subproc(self,*args,**kwargs):
        subprocess.run(*args,**kwargs)
    
    @classmethod
    def service(cls,cmd:str,terminal:str=None):
        """select the way for starting an external service"""

        if terminal is None: terminal=_config_["terminal"]
        assert _config_["terminal"] in "xterm|winterm|wsl"

        if terminal == "winterm":
            # start an external service within Windows Terminal
            os.system(f'cmd.exe /c start wt wsl {cmd} &')
        
        elif terminal == "wsl":
            # start an external service using wsl command
            subprocess.run(
                f'cmd.exe /c start wsl {cmd} &',
                stderr=subprocess.DEVNULL, shell=True)

        elif terminal == "xterm":
            # start an external service within xterm
            os.system("%s xterm -C -geometry 190x19 -e %s &"
                % (_config_["display"], cmd))

    def cmd(self,**kwargs) -> str:
        """return bash command for running server"""
        raise NotImplementedError

    def run_local(self,service=False):
        # expected pattern
        if service: pass
        else: pass
        raise NotImplementedError

    def run_server(self,service=False):
        raise NotImplementedError

    def commandLine(self,args):
        """provide function for the command line interface"""
        raise NotImplementedError


class MongoDB(BaseService):

    def __init__(self,*args,**kwargs):
        super(MongoDB,self).__init__(*args,**kwargs)

        self.client = None
        self.database = None
        self.dbpath = _config_["db_path"]
        self.is_local = _config_["db_host"]=="localhost"

    def cmd(self,dbpath) -> str:
        """provide the mongod bash command"""
        return f'mongod --dbpath="{dbpath}"'

    def run_local(self,service=False):
        #FIXME: skip when needed
        if not self.is_local: return

        cmd = self.cmd(dbpath=self.dbpath)
        if service: self.service(cmd)
        else: self.subproc(cmd,shell=True)
        echo("the MongoDB server is running at 'localhost'")       
        
    def set_client(self,select:str):
        from pymongo import MongoClient
        
        echo("try for getting mongodb client...")
        self.client = MongoClient(host=self.host,port=self.port)

        echo("available databases given by mongoclient:",
            self.client.list_database_names() )

        self.database = self.client[select]
        
        echo("connected to the default database:",
            "'%s'"% _config_["db_select"] )
        echo("existing mongodb collections:",
            self.database.list_collection_names() )
    
    def commandLine(self,args):
        self.run_local(service=False)


class JupyterLab(BaseService):

    locker = 0
    def __init__(self,*args,**kwargs):
        super(JupyterLab,self).__init__(*args,**kwargs)

        from urllib.parse import urljoin
        self.lab_host = urljoin(self.url,"lab")
        self.nbk_host = urljoin(self.url,"tree")

    def cmd(self,directory):
        """provide the jupyterlab bash command"""
        return f"{_py3_} -m jupyterlab --no-browser --notebook-dir={directory}"

    def run_local(self,directory=None,service=False):
        # ensure that only one jupyter server is running
        if self.locker: return
        else: self.locker = 1
        # set working/notebook root directories
        os.chdir(os.environ["HOME"])
        if not directory: directory=_config_["notebook_dir"]
        # start jupyterlab server
        echo("start the enhanced jupyterlab server")
        cmd = self.cmd(directory=directory)
        if service: self.service(cmd)
        else: self.subproc(cmd,shell=True)
    
    def set_ipykernel(self):
        """set sweetenv ipython kernel for running jupyter"""
        os.chdir(f"/opt/{_project_}/programs")
        echo("set sweetenv.py kernel for running jupyter")
        self.subproc(
            f"{_py3_} -m ipykernel install --user --name=sweetenv.py",
            shell=True )

    def set_password(self):
        #NOTE: this method exists to be used into ini.__init__
        # _py3_ must be re-evaluted within the init process
        self.subproc(
            f"{_py3_} -m jupyter notebook password -y",
            shell=True )

    def commandLine(self,args):
        if args.password:
            self.set_password()
        if args.set_kernel:
            self.set_ipykernel()
        if args.lab:
            webbrowser(self.lab_host)
        elif args.notebook:
            webbrowser(self.nbk_host)

        if args.home: dir= os.environ["HOME"]
        else: dir= _config_["notebook_dir"]
        self.run_local(directory=dir,service=False)
        sys.exit()


class Uvicorn(BaseService):

    def __init__(self,*args,**kwargs):
        super(Uvicorn,self).__init__(*args,**kwargs)

        # set uvicorn arguments dict
        self.uargs = {
            "host": self.host,
            "port": self.port,
            "log_level": "info" }

    def cmd(self,app:str="") -> str:
        return f"sweet run-uvicorn {app}"

    def run_local(self,app="",service=None):
        """run the uvicorn webserver
        app argument can be 'str' or 'Starlette' object"""

        if service is None: service = multi_threading
        if service is True: self.service(self.cmd(app))

        elif service is False:
            os.chdir(_config_['working_dir'])
            if not app: app = webapp.star
            from uvicorn import run
            run(app,**self.uargs)

        else: raise TypeError

    def commandLine(self,args):
        self.run_local(args.app,service=False)


class MdBook(BaseService):
    """for using mdBook command line tool
    a Rust crate to create books using Markdown"""

    def __init__(self,*args,**kwargs):
        super(MdBook,self).__init__(*args,**kwargs)

    def cmd(self,args:str):
        """return mdbook bash command prefixed with path"""
        #FIXME: overcome PATH matter
        ini.PATH(_deepconfig_["rust-crates"])

        return f"{_deepconfig_['rust-crates']}/mdbook {args}"

    def commandLine(self,args):
        """provide mdBook tools via the 'sweet' command line interface"""

        if not args.name:
            echo("no book name given, default settings applied")

        if args.anywhere: directory= os.path.join(os.getcwd(),args.name)
        else: directory= f"/opt/{_project_}/documentation/{args.name}"
        isbook= os.path.isfile(os.path.join(directory,"book.toml"))

        if args.build:
            # init/build book within current directory:
            self.init(directory)
            self.build(directory)

        elif args.newbook:
            # init book within directory without building it:
            self.init(directory)

        elif not args.open and not args.name:
            # open the default book of the project:
            self.open()

        elif not isbook:
            if args.name: msg= f"Error, book '{args.name}' not existing"
            else: msg= f"WARNING: root book not existing within documentation"
            echo(msg, mode="exit")
        
        elif args.name: args.open=True
        
        if args.open:
            #FIXME: provide default settings:
            if directory==_config_["working_dir"]: bkdir="markdown_book"
            else: bkdir="book"
            # open book for given directory:
            path = os.path.join(directory,bkdir,"index.html")
            self.open(path)

    def init(self,directory:str):
        """init a new mdbbok within given directory"""

        # check if a doc is existing and create it if not:
        if not os.path.isfile(os.path.join(directory,"book.toml")):
            echo("init new mdBook within directory:",directory)
            self.subproc(self.cmd(f"init --force {directory}"),shell=True,
                capture_output=True, text=True, input=_config_["gitignore"])

    def build(self,directory:str=""):
        echo("build mdBook within directory:",directory)
        self.subproc(self.cmd(f"build {directory}"),shell=True)

    def open(self,path:str=""):
        if not path: path= _config_["webbook"]
        echo("open built mdBook:",path)
        webbrowser(path)

    def run_local(self,directory:str=""):
        if not directory: directory= _config_["working_dir"]
        echo("start the rust mdbook server")
        self.service(
            self.cmd(f"serve -n {self.host} -p {self.port} {directory}"))


#############################################################################
 ########## CHERRYPY FACILITIES ##############################################
  #############################################################################

try:
    import cherrypy
    ConfigAccess.cherrypy = True

    class CherryPy(BaseService):
        """provide cherrypy server facilities

        cherrypy can be used optionnaly for serving static contents
        such server is very stable and keeps performances at high level
        """

        def __init__(self,*args,**kwargs):
            super(CherryPy,self).__init__(*args,**kwargs)

        def cmd(self) -> str:
            return f"{_py3_} -m sweet -p {_project_} run-cherrypy"

        def run_local(self,service=False):
            if service: self.service(self.cmd())
            else: self.start(webapp)

        @classmethod
        def commandLine(self, args):
            self.start(webapp)

        # re-implement here some usual cherrypy objects:
        serve_file = cherrypy.lib.static.serve_file

        # abstract setting multi-apps config:
        @classmethod
        def setconfig(cls, config: dict):
            """set or update configuration files to use for apps
            allow replacement of the default configuration file too

                setconfig({
                    "/": "/path/to/default/configuration/file",
                    "/another": "/path/to/another/configuration/file",
                })

            mount() MUST be called afterwards

                mount({
                    "/": MyRootApp(),
                    "/another": AnotherApp(),
                )}

            at last the start() function will start mounted apps with setted configs

                start()
            """
            _config_["cherrypy"].update(config)

        # abstract mounting multi-apps:
        @classmethod
        def mount(cls, routing, url="/", config=None):
            """convenient function for mounting different apps running with cherrypy
            you should consider using setconfig() for settings different configurations

                mount({
                    "/": MyRootApp(),
                    "/another": AnotherApp(),
                )}

            OR can be used for mounting a single app too for differing start() call
            see the cherrypy.tree.mount documentation for better understanding

                mount("/location", "/", "/path/to/configuration/file")
                start()
            """
            if isinstance(routing, dict):
                for segment, object_ in routing.items():

                    cherrypy.tree.mount(
                        object_,
                        segment,
                        _config_["cherrypy"].get(segment, None) )

            else:
                if config is None: config=_config_["cherrypy"]["/"]
                cherrypy.tree.mount(routing, url, config)

        # abstract mounting REST dispatching:
        @classmethod
        def dispatch(cls, dispatch_routing: dict):
            """convenient function for configurating REST dispatching with cherrypy
            works for many url segments to dispatch (segments = keys of the dict)

                dispatch({
                    "/dispatched/url": { 
                    "GET": get_function_name,
                    "POST": post_function_name,
                    "PUT": put_function_name,
                    "DELETE": delete_function_name } 
                })
            """
            for segment, methods in dispatch_routing.items():

                cherrypy.tree.mount(
                    CherryHttpDispatcher(methods),
                    segment,
                    _config_["cherrypy"].get(
                        segment,
                        {"/": {"request.dispatch": 
                            cherrypy.dispatch.MethodDispatcher()}} ))

        # start web apps and listen for requests:
        @classmethod
        def start(cls, route=None, url="/", config=None):
            """start the previously mounted apps with mount()

            OR when the route argument is given this function is
            equivalent to cherrypy.quickstart(route, url, config)
            it provides the default setted configuration for the root segment "/"

            AT LAST use stop() to stop de server started with start()
            """
            print("run cherrypy webserver: press ctrl-C to quit")

            if route is None:
                # cherrypy.config.update({'server.socket_host': '0.0.0.0', })
                # cherrypy.config.update({'server.socket_port': port, })
                cherrypy.engine.start()
                cherrypy.engine.block()
            else:
                if config is None: config=_config_["cherrypy"]["/"]
                cherrypy.quickstart(route, url, config)

        # stop the web application
        @classmethod
        def stop(cls):
            cherrypy.engine.stop()

    # abstract the cherrypy dispatch recipe:
    @cherrypy.expose
    class CherryHttpDispatcher:
        """set related function for each http methods as follow:

            HttpDispatcher({
                "GET": get_function,
                "POST": post_function,
                "PUT":  put_function,
                "DELETE": delete_function })
        """
        def __init__(self, methods):
            self.methods = methods

        @cherrypy.tools.accept(media="text/plain")
        def GET(self, *args, **kwargs):
            self.methods["GET"](*args, **kwargs)

        def POST(self, *args, **kwargs):
            self.methods["POST"](*args, **kwargs)

        def PUT(self, *args, **kwargs):
            self.methods["PUT"](*args, **kwargs)

        def DELETE(self, *args, **kwargs):
            self.methods["DELETE"](*args, **kwargs)

    # set a default CherryPy instance:
    #FIXME: only for test
    staticserver = CherryPy(url=static_host)

except:
    class cherrypy:
        """implement cherrypy.expose as a ghost method"""
        @classmethod
        def expose(*args):
            pass
