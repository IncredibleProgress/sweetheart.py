"""sweet.py
get coding full power at the speedlight"""

__version__ = "0.1.0-dev8"
__license__ = "CeCILL-C"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"


import os, subprocess

#NOTE: import
# - main modules import are within the WEBAPP FACILITIES section
# - cherrypy import is within the CHERRYPY FACILITIES section
# - pymongo import is within the subroc.mongod method
# - some modules import from standard libs are within relevant objects


# hardcoded default settings:
# allow setting of 2 webservers respectively for data and statics
async_host = "http://127.0.0.1:8000"# uvicorn webserver
static_host = "http://127.0.0.1:8080"# cherrypy webserver
mongo_disabled = False


# provide messages function for convenience:
#NOTE: allow message management improvements later
def echo(*args):
    """convenient function for printing messages"""
    print(_config_["bash"]["echolabel"], *args)


  #############################################################################
 ########## CONFIGURATION ####################################################
#############################################################################

# allow dedicated config for dev purpose
if os.environ["PWD"].startswith("/opt/incredible"): _project_="incredible"
else: _project_="sweetheart"

# provide the default configuration:
# should be updated using _config_.update({ "key": value })
_config_ = {
    "database": {
        "host": "localhost",
        "port": 27017,
        "dbpath": f"/opt/{_project_}/database",
        "select": "demo",
    },
    "webapp": {
        "framework": "starlette",# starlette|responder|fastapi
        #"AI": "scikit-learn",
        "working_dir": f"/opt/{_project_}/webpages",
        "templates_dir": "bottle_templates",

        "settings": {
            "_default_libs_": "knacss py",
            "_static_": "",# ""=disabled
            "_async_": async_host,
        }
    },
    "cherrypy": {
        # set default url segments configs:
        "/": f"/opt/{_project_}/configuration/cherrypy.conf",
    },
    "bash": {
        "echolabel": "[SWEETHEART]",
        "display": "DISPLAY=:0",
        "service": "winterm",# xterm|winterm
        "webapp": f"cmd.exe /c start msedge.exe --app={async_host}",
        "cherry": f"/opt/{_project_}/programs/envPy/bin/python3 -m\
            sweet run-cherrypy",
    },
    "copyfiles": {
        # used within the init() function
        # provided config files:
        "cherrypy.conf": f"/opt/{_project_}/configuration",
        "config.xlaunch": f"/opt/{_project_}/configuration",
        # provided templates:
        "login.txt": f"/opt/{_project_}/webpages/bottle_templates",
        "document.txt": f"/opt/{_project_}/webpages/bottle_templates",
        # provided documents:
        "welcome.md": f"/opt/{_project_}/webpages/markdown_docs",
        # provided resources:
        "sweet.HTML": f"/opt/{_project_}/webpages",
        "favicon.ico": f"/opt/{_project_}/webpages/usual_resources",
        "sweetheart-logo.png": f"/opt/{_project_}/webpages/usual_resources",
    },
    "pcloud": {
        # pcloud settings (for dev purpose):
        "local": "/mnt/p/Public Folder/sweetheart",
        "public": "https://filedn.eu/l2gmEvR5C1WbxfsrRYz9Kh4/sweetheart/",
        "mount": "sudo mount -t drvfs p: /mnt/p",
    },
}


class config_accessor:

    def __init__(self, config_object_name:str):
        """provide a convenient config accessor tool"""

        self.config = config_object_name
        self.verbosity = None

    def __getitem__(self, keys:str):
        """
        "key1.key2" -> self.config["key1"]["key2"]
        "key1.key2.key3" -> self.config["key1"]["key2"]["key3"]
        """
        item = f"{self.config}{self.ksplit(keys)}"

        if self.verbosity:
            echo("get item via config_accessor", item)

        return eval(item)
    
    @staticmethod
    def ksplit(keys):
        # ksplit("key1.key2") -> str: "['key1']['key2']"
        return "".join([f"['{key}']" for key in keys.split(".")])


_ = CONF = config_accessor("_config_")
# _["key1.key2"] -> _config_["key1"]["key2"]


# provide some config shorcuts for readability:
# set pre-defined config values with readable names for better clarity
static_host_disabled = _config_["webapp"]["settings"]["_static_"]==""


  #############################################################################
 ########## EXTERNAL SERVICES FACILITIES #####################################
#############################################################################

class subproc:
    """tools for executing linux shell commands:
    >>> subproc.bash("command line")
    >>> subproc.run(["list","of","bash","intruc"])
    >>> subproc.service("command line")
    """
    bash = lambda s: subprocess.run(s.split())
    run = subprocess.run

    @staticmethod
    def xterm(cmd:str):
        """start an external service within xterm"""
        os.system("%s xterm -C -geometry 190x19 -e %s &"
            % (_config_["bash"]["display"], cmd))

    @staticmethod
    def winterm(cmd:str):
        """start an external service within Windows Terminal"""
        subproc.bash(f'cmd.exe /c start wt.exe ubuntu.exe run {cmd}')

    # select the way for starting external service:
    # used for starting mongod and cherrypy within external terminal
    service = eval(_config_["bash"]["service"])

    @classmethod
    def mongod(cls):
        """abstract mongoDB settings"""
        global mongoclient, database

        from pymongo import MongoClient
        
        echo("try for getting mongodb client...")
        cls.service(
            'mongod --dbpath="%s"'\
            % _config_["database"]["dbpath"] )

        mongoclient = MongoClient(
            host=_config_["database"]["host"],
            port=_config_["database"]["port"] )

        echo("available databases given by mongoclient:",
            mongoclient.list_database_names() )

        database = mongoclient[_config_["database"]["select"]]
        
        echo("connected to the default database:",
            "'%s'"% _config_["database"]["select"] )
        echo("existing mongodb collections:",
            database.list_collection_names() )


class pcloud:

    @staticmethod
    def update_files():
        echo("update init files provided from pcloud")

        for filename, path in _config_["copyfiles"].items():
            if filename.startswith("_"): continue

            source = os.path.join(path, filename)
            dest = _config_["pcloud"]["local"]

            if argv.verbosity:
                print(" ", source, " -> ", dest)

            if not os.path.isdir(_config_["pcloud"]["local"]):
                subproc.bash(_config_["pcloud"]["mount"])

            subproc.run(["cp", source, dest])


  #############################################################################
 ########## COMMAND LINE INTERFACE ###########################################
#############################################################################

def cli():
    """build the sweetheart command line interface (CLI)"""

    import argparse
    global argv, mongo_disabled

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.set_defaults(func= lambda args:\
        print("for getting some help use the '--help' option"))

    parser.add_argument("-v","--verbosity",action="store_true",
        help="get some additional messages about processing" )

    parser.add_argument("-i","--init",action="store_true",
        help="launch the init process for building the sweetheart venv")


    # FIXME: ugly dev tools:
    parser.add_argument("--update-pcloud",action="store_true")


    # create the parser for the "start" command:
    start = subparsers.add_parser("start",
        help="start all required services for running webapps")

    start.add_argument("-x","--mongo-disabled",action="store_true",
        help="start without the mongo database server")

    start.add_argument("-a","--webapp",action="store_true",
        help="start within webbrowser as an app")

    start.add_argument("-c","--cherrypy",action="store_true",
        help="start running cherrypy as an extra webserver for statics")

    start.set_defaults(func= lambda args: quickstart())


    # create the parser for the "docmaker" command:
    docmkr = subparsers.add_parser("docmaker",
        help="build html static documentation from markdown files")
   
    docmkr.set_defaults(func= lambda args: docmaker())
    

    # create the parser for the "run-cherrypy" command:
    cherry = subparsers.add_parser("run-cherrypy",
        help="run the cherrypy webserver for statics")

    cherry.set_defaults(func= lambda args: CherryPy.start(webapp))


    argv = parser.parse_args()

    # disable mongoclient setting when required:
    if hasattr(argv,"mongo_disabled") and argv.mongo_disabled:
        mongo_disabled = True
    
    # update config_accessor attributes:
    config_accessor.verbosity = argv.verbosity
    
    return argv


def init():
    """ init a new sweetheart project """

    from urllib.parse import urljoin

    # start install process:
    print("\n[SWEETHEART] init process start now !")
    print("root privileges are required to continue")
    print("an internet connexion is required for downloads")
    print("\nINIT step1: install required packages...\n")
    subproc.run([
        "sudo","apt","install",

            "python3-venv",
            "mongodb",
            "xterm",
            #"git",
            "npm",
            "node-typescript",
            "node-vue",
            "libjs-vue",
            "libjs-highlight.js",
            "libjs-bootstrap4",  
            "libjs-jquery",
        ])
    print("\nINIT step2: creating directories...")
    subproc.bash("sudo mkdir /opt/sweetheart")
    subproc.bash("sudo mkdir /opt/sweetheart/configuration")
    subproc.bash("sudo mkdir /opt/sweetheart/database")
    subproc.bash("sudo mkdir /opt/sweetheart/documentation")
    subproc.bash("sudo mkdir /opt/sweetheart/programs")
    subproc.bash("sudo mkdir /opt/sweetheart/programs/scripts")
    subproc.bash("sudo mkdir /opt/sweetheart/webpages")
    subproc.bash("sudo mkdir /opt/sweetheart/webpages/bottle_templates")
    subproc.bash("sudo mkdir /opt/sweetheart/webpages/markdown_docs")
    subproc.bash("sudo mkdir /opt/sweetheart/webpages/usual_resources")
    subproc.bash("sudo chmod 777 -R /opt/sweetheart")

    subproc.bash(
        "ln --symbolic /usr/share/javascript \
        /opt/sweetheart/webpages/javascript_libs" )

    print("\nINIT step3: building python env...\n")
    subproc.bash("python3 -m venv /opt/sweetheart/programs/envPy")
    subproc.run([
        "/opt/sweetheart/programs/envPy/bin/python3","-m",
        "pip","install",

            "sweetheart",
            "pymongo",
            #"cherrypy",
            "uvicorn",
            "aiofiles",#NOTE: required with starlette
            "bottle",
            "mistune",
            #"openpyxl",
            *_["webapp.framework"].split()
        ])
    print("\nINIT step4: downloading resources...\n")

    os.chdir("/opt/sweetheart/webpages/usual_resources")
    for url in [
        "https://raw.githubusercontent.com/alsacreations/KNACSS/master/css/knacss.css",
        "https://www.w3schools.com/w3css/4/w3.css" ]:
        print("download file:", url)
        subproc.run(["wget","-q","--no-check-certificate",url])

    pcloud = lambda file: urljoin(_["pcloud.public"], file)

    for file, path in _config_["copyfiles"].items():
        if file.startswith("_"): continue
        print("download file:", pcloud(file))
        os.chdir(path.replace(_project_, "sweetheart"))#!
        subproc.run(["wget","-q","--no-check-certificate", pcloud(file)])

    print("\nINIT step5: downloading node modules...\n")
    os.chdir("/opt/sweetheart/webpages")
    subproc.bash("npm init --yes")
    subproc.run([
        "npm","install",

            #NOTE: brython could be installed too as python package with pip
            "brython"
        ])
    print("\nINIT step6: provide local bash commands...\n")
    os.chdir("/opt/sweetheart/programs/scripts")

    with open("sweet","w") as fo:
        L1= "#!/bin/sh"
        L2= "/opt/sweetheart/programs/envPy/bin/python3 -m sweet $*"
        fo.write(f"{L1}\n{L2}")

    subproc.bash("sudo ln --symbolic \
        /opt/sweetheart/programs/scripts/sweet /usr/local/bin/")
    subproc.bash("sudo chmod 777 /usr/local/bin/sweet")


if __name__ == "__main__":

    # build the Command Line Interface
    # launch the "init" process if required before modules import
    argv = cli()
    if argv.update_pcloud: pcloud.update_files()
    if argv.init: init()


  #############################################################################
 ########## CHERRYPY FACILITIES ##############################################
#############################################################################

try:
    import cherrypy

    class CherryPy:
        """provide a namespace for cherrypy facilities

        cherrypy seems to be very used for serving static content
        this server is very stable and keeps performances at high level
        """

        # re-implement some usual cherrypy objects:
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
            """
            start the previously mounted apps with mount()

            OR when the route argument is given this function is
            equivalent to cherrypy.quickstart(route, url, config)
            it provides the default setted configuration for the root segment "/"

            AT LAST use stop() to stop de server started with start()
            """
            print("press ctrl-C to quit")

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


except:
    echo("cherrypy is not implemented for current config")
    class cherrypy:
        """implement cherrypy.expose as a ghost method"""
        @classmethod
        def expose(*args):
            pass


  #############################################################################
 ##########  WEBAPP FACILITIES ###############################################
#############################################################################

from bottle import template
from mistune import markdown
from collections import UserList, UserDict

import uvicorn
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, FileResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

###############################################################################
###############################################################################

# convenient function for rendering html content:
def html(source:str= "WELCOME", **kwargs):

    if source == "WELCOME":
        # provide a welcome message:
        user = os.environ["USER"].capitalize()
        return HTMLResponse(f"""
            <link rel="stylesheet" href="/resources/knacss.css">
            <div class="txtcenter">
            <h1><br><br>Welcome {user} !<br><br></h1>
            <h3>sweetheart.py</h3>
            <p>a supercharged heart for the non-expert hands</p>
            <p>be aware that you could fall in love with it</p>
            <p><a href="{async_host}/document/welcome" 
                class="btn" role="button">go farer ahead now !</a></p>
            <p><br><br><br><em>this message appears because there
                was nothing else to render here</em></p>
            </div>""")

    template_path = os.path.join(_["webapp.templates_dir"], source)
    if os.path.isfile(template_path):

        # render html content from given bottle template:
        return HTMLResponse(template(
            template_path,
            **_config_["webapp"]["settings"],
            **kwargs ))

    elif source.endswith(".md") and os.path.isfile(source):

        # render html content from given markdown file:
        with open(source) as file:
            return HTMLResponse(template(
                os.path.join(_["webapp.templates_dir"],"document.txt"),
                text= markdown(file.read()),
                **_config_["webapp"]["settings"],
                **kwargs ))

    elif "</" in source:
        #FIXME: not so good for detecting html content!
        # render here the source as a pure html content
        return HTMLResponse(source)

    raise ValueError("invalid source argument calling html()")


# convenient function for starting a webapp
def quickstart(routes=None, endpoint=None):
    """start webapp on ASGI web server
    include a default routing settings for the webpages directory"""
    global webapp

    # at first set and start mongo database service:
    if not mongo_disabled: subproc.mongod()
    else: echo("MongoDB client is DISABLED")

    # set the current working directory:
    os.chdir(_config_["webapp"]["working_dir"])
    echo("set working directory:", os.getcwd())
    
    # then build routing depending of given arguments:
    if isinstance(routes, dict):
        echo("create and route starlette objects from dict")
        for segment,endpoint in routes.items():
            webapp.append( Route(segment,endpoint) )

            if argv.verbosity:
                print("  callable segment:",callable(endpoint),"",segment)

    elif isinstance(routes, str) and callable(endpoint) :
        echo("route directly given html content at /")
        webapp.append( Route("/", lambda request: html(routes)) )

    elif routes is None and endpoint is None:
        echo("route a default welcome message at", async_host)
        webapp.append( Route("/", welcome) )

    elif routes is None and isinstance(endpoint, function):
        echo("route a single webpage at", async_host)
        webapp.append( Route("/", routes) )
    else:
        raise ValueError("invalid given arguments")

    if argv.cherrypy:
        # start cherrypy as external service:
        # this will happen with bash command 'sweet -c start'
        echo("try running cherrypy webserver as external service")
        subproc.service(_config_["bash"]["cherry"])

        if static_host_disabled:
            _config_["webapp"]["settings"]["_static_"] = static_host

        echo("run static host with given config:",
            _config_["webapp"]["settings"]["_static_"])

    # set routing and create Starlette object:
    webapp.mount(route_options=True)

    if argv.verbosity:
        echo("list of routed objects type for check: ")
        for i, route in enumerate(webapp):
            print(" ",i+1, "  type:", type(route))
    
    # auto start the webapp within webbrowser:
    if hasattr(argv,"webapp") and argv.webapp:
        subproc.bash( _config_["bash"]["webapp"] )

    # at last start the uvicorn webserver:
    echo("quickstart: uvicorn multi-threading is not available here")
    uvicorn.run(webapp.star, log_level="info")


class WebApp(UserList):

    # default urls endpoints:
    #NOTE: the 'request' argument is required for rendering methods
        
    def index(self, request):
        return html("login.txt")

    def document(self, request):
        filename = request.path_params["filename"]
        return html(f"markdown_docs/{filename}.md")
    
    def favicon(self, request):
        return FileResponse("usual_resources/favicon.ico")

    # webapp settings:
    # class methodes for main settings: mount() star()

    def mount(self, route_options=True):
        """set optionnal routing and mount static dirs"""

        # route options if required:
        if route_options: 
            self.extend([
                Route("/favicon.ico", self.favicon),
                Route("/document/{filename}", self.document),
            ])
        # mount static resources:
        self.extend([
            Mount("/resources", StaticFiles(directory="usual_resources")),
            Mount("/libs", StaticFiles(directory="javascript_libs")),
            Mount("/modules", StaticFiles(directory="node_modules")),
        ])
    
    @property
    def star(self) -> Starlette:
        # typical use: uvicorn.run(webapp.star)
        self.mount(route_options=True)
        return Starlette(debug=True, routes=self)

    # allow serving statics with cherrypy:
    # optional facility for increase of performance

    @cherrypy.expose
    def default(self):
        return """
        <link rel="stylesheet" href="/resources/knacss.css">
        <div class="txtcenter">
        <h1><br><br>I'm Ready<br><br></h1>
        <h3>cherrypy server is running</h3>
        <p>for better performances serving static files</p>
        </div>"""

    @cherrypy.expose
    def static(self):
        #FIXME: not yet implemented
        return CherryPy.serve_file()


# convenient features for building webapp:
webapp = WebApp()
routing = lambda routes: webapp.extend(routes)
welcome = lambda request: html("WELCOME")


  #############################################################################
 ##########  DOCUMENTATION FACILITIES ########################################
#############################################################################

def docmaker():
    """FIXME: only for test"""

    source_dir = f"/opt/{_project_}/webpages/markdown_docs"
    dest_dir = f"/opt/{_project_}/documentation"
    os.chdir(f"/opt/{_project_}/webpages")
    echo("build doc from:",source_dir,"to:",dest_dir)

    with os.scandir(source_dir) as iterator:
        for entry in iterator:
            if entry.is_file() and entry.name.endswith('.md'):

                source= entry.path
                dest= os.path.join(dest_dir,entry.name.replace('.md','.html'))
                
                with open(source,'r') as fi:
                    tpl = template(
                        os.path.join(_["webapp.templates_dir"],"document.txt"),
                        text= markdown(fi.read()),
                        **_config_["webapp"]["settings"])

                with open(dest,'w') as fo:
                    fo.write(tpl)


###############################################################################
###############################################################################

if __name__ == "__main__":

    # provide the available public objects list:
    if argv.verbosity:

        objects = dict( (k,v) for k,v in globals().items() \
            if k[0] != "_" and not repr(v).startswith("<module") )

        echo("available objects provided by sweet.py:")
        import pprint
        pprint.pprint(objects)
    
    # execute dedicated function related to the cli:
    argv.func(argv)
