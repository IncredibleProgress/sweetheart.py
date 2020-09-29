'''
provide simple use of highest quality components
for building full-stacked webapps including AI

    import sweet

    def welcome():
        """render a welcome message"""
        return sweet.html()

    sweet.quickstart(welcome)
'''

__version__ = "0.1.0-beta2"
__license__ = "CeCILL-C"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"


import os, subprocess, json

#NOTE: import
# - main modules import are within the WEBAPP FACILITIES section
# - cherrypy import is within the CHERRYPY FACILITIES section
# - pymongo import is within the subroc.mongod method
# - some modules import from standard libs are within relevant objects


# hardcoded default settings for services:
# allow setting of 2 webservers respectively for data and statics

async_host = "http://127.0.0.1:8000"# uvicorn webserver
static_host = "http://127.0.0.1:8080"# cherrypy webserver

mongo_disabled = False
cherrypy_enabled = False
multi_threading = False


# allow dedicated configs for dev purpose:
_dir_ = os.path.split(os.environ["PWD"])
if _dir_[0] == "/opt" and _dir_[1]: _project_ = _dir_[1]
else: _project_ = "sweetheart"
_py3_ = f"/opt/{_project_}/programs/envPy/bin/python3"


  #############################################################################
 ########## CONFIGURATION ####################################################
#############################################################################

# provide the default configuration:
# should be updated using _config_.update({ "key": value })
_config_ = {

    ## webapps settings:
    "config_path": (f"/opt/{_project_}/configuration", "sweet.json"),
    "working_dir": f"/opt/{_project_}/webpages",
    "docs_dir": f"/opt/{_project_}/documentation",
    
    "web_framework": "starlette",# starlette|fastapi
    "templates_dir": "bottle_templates",
    "templates_settings" : {

        "_default_libs_": "knacss py",
        "_static_": "",# ""=disabled
        "_async_": async_host,
    },
    
    "cherrypy": {
        # set default url segments configs:
        "/": f"/opt/{_project_}/configuration/cherrypy.conf",
    },
    
    ## database settings:
    "db_host": "localhost",
    "db_port": 27017,
    "db_path": f"/opt/{_project_}/database",
    "db_select": "demo",

    ## bash settings:
    "echolabel": _project_,
    "display": "DISPLAY=:0",
    "terminal": "winterm",# xterm|winterm

    "sh_venv": _py3_,
    "sh_webapp": f"cmd.exe /c start msedge.exe --app={async_host}",
    "sh_cherrypy":f"{_py3_} -m sweet run-cherrypy",
    "sh_opendocs": f"cmd.exe /c start msedge.exe --app=\
\\\\wsl$\\Ubuntu\\opt\\{_project_}\\documentation\\site\\index.html",

    "scripts": {
        #"bdist": f"{_py3_} setup.py sdist bdist_wheel",
        #"upload": f"{_py3_} -m twine upload dist/*",
        "pkgtools": f"{_py3_} -m pip install setuptools twine wheel",
    },
    
    ## pcloud settings (for dev purpose):
    "pmount": "sudo mount -t drvfs p: /mnt/p",
    "cloud_local": "/mnt/p/Public Folder/sweetheart",
    "cloud_public": "https://filedn.eu/l2gmEvR5C1WbxfsrRYz9Kh4/sweetheart/",

    "copyfiles": {
        # given here for the init() function
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
}

class _config_accessor_:
    """provide a convenient _config_ accessor tool"""

    conffile = os.path.join(*_config_["config_path"])
    conffile = conffile if os.path.isfile(conffile) else None
    copyfiles = _config_["copyfiles"]; del _config_["copyfiles"]

    # uvicorn arguments dict:
    uargs = {
        "host": async_host.split(":")[1].strip("/"),
        "port": int(async_host.split(":")[2]),
        "log_level": "info" }

    # general settings given within CLI:
    verbosity = False
    webapp = False
    cherrypy = False

    def __getitem__(self, keys:str):
        ''' _["key1.key2"] -> _config_["key1"]["key2"] '''
        verbose("get config item:", keys)
        ksplit = lambda keys:\
            "".join([f"['{key}']" for key in keys.split(".")])
        return eval( f"_config_{ksplit(keys)}" )
    
    @classmethod
    def edit(cls):
        # edit _config_ as json configuration file
        with open(cls.conffile, "w") as fo:
            fo.write(json.dumps(_config_, indent=2))

_ = conf = _config_accessor_()


_msg_ = []
def echo(*args, mode="default"):
    """convenient function for printing messages
    mode = 0|default|stack|release"""

    if mode == "stack" or mode == 0:
        global _msg_
        _msg_.append(" ".join(args))

    elif mode == "release":
        for msg in _msg_:
            print("[%s]"% _config_["echolabel"].upper(), msg)
        _msg_ = []
    else:
        print("[%s]"% _config_["echolabel"].upper(), *args)


def verbose(*args):
    """convenient function for verbose messages"""
    if _.verbosity: print(" ", *args)


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
            % (_config_["display"], cmd))

    @staticmethod
    def winterm(cmd:str):
        """start an external service within Windows Terminal"""
        os.system(f'cmd.exe /c start wt.exe ubuntu.exe run {cmd} &')

    # select the way for starting external service:
    # used for starting mongod, cherrypy, uvicorn within external terminal
    service = eval(_config_["terminal"])

    @classmethod
    def mongod(cls):
        """abstract mongoDB settings"""
        global mongoclient, database

        from pymongo import MongoClient
        
        echo("try for getting mongodb client...")
        cls.service(
            'mongod --dbpath="%s"'\
            % _config_["db_path"] )

        mongoclient = MongoClient(
            host=_config_["db_host"],
            port=_config_["db_port"] )

        echo("available databases given by mongoclient:",
            mongoclient.list_database_names() )

        database = mongoclient[_config_["db_select"]]
        
        echo("connected to the default database:",
            "'%s'"% _config_["db_select"] )
        echo("existing mongodb collections:",
            database.list_collection_names() )


class cloud:
    
    @staticmethod
    def update_files():
        #FIXME: dev tool not for use
        echo("updating init files provided from pcloud...")
        for filename, path in _.copyfiles.items():

            source = os.path.join(path, filename)
            dest = _config_["cloud_local"]
            verbose(source, " -> ", dest)

            if not os.path.isdir(_config_["cloud_local"]):
                subproc.bash(_config_["pmount"])

            subproc.run(["cp", source, dest])
        echo("all updates done to the pcloud drive")


  #############################################################################
 ########## COMMAND LINE INTERFACE ###########################################
#############################################################################

def cli():
    """build the sweetheart command line interface (CLI)"""

    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.set_defaults(func= lambda args: print("* sweet.py: \
use the '--help' or '-h' option for getting some help"))

    parser.add_argument("-v","--verbosity",action="store_true",
        help="get some additional messages about process" )

    parser.add_argument("-i","--init",action="store_true",
        help="launch the init process for building the sweetheart env")

    parser.add_argument("-cf","--conffile",action="store_true",
        help="load config from sweet.json config file" )
    
    parser.add_argument("--venv", action="store_true",
        help="python3 within the virtual env built for sweetheart")

    parser.add_argument("--edit-config", action="store_true",
        help="provide a default configuration json file")

    #FIXME: provisional dev tools:
    parser.add_argument("--update-pcloud", action="store_true")


    # create the parser for the "cmd" command:
    src = subparsers.add_parser("cmd",
        help="execute a script given by the current config")

    src.add_argument("script",
        help=f'name of a script given in _config_:\
            {[i for i in _config_["scripts"].keys()]}')

    def _exec(args):
        cmd = _config_["scripts"][f"{args.script}"]
        echo("bash:$", cmd)
        subproc.bash(cmd)

    src.set_defaults(func=_exec)


    # create the parser for the "start" command:
    start = subparsers.add_parser("start",
        help="start required services for running webapps")

    start.add_argument("-x","--mongo-disabled",action="store_true",
        help="start without the mongo database server")

    start.add_argument("-a","--webapp",action="store_true",
        help="start within the webbrowser as an app")

    start.add_argument("-c","--cherrypy",action="store_true",
        help="start cherrypy as an extra webserver for static contents")
    
    start.add_argument("-m","--multi-threading",action="store_true",
        help="start uvicorn webserver allowing multi-threading")

    start.set_defaults(func= lambda args: quickstart())


    # create the parser for the "mkdocs" command:
    mdoc = subparsers.add_parser("mkdocs",
        help="build html documentation from markdown files")
    
    mdoc.add_argument("-o","--open",action="store_true",
        help="open documentation in webbrowser after building it")
   
    mdoc.set_defaults(func= lambda args: mkdocs())


    # create the parser for the "run-cherrypy" command:
    cherry = subparsers.add_parser("run-cherrypy",
        help="run cherrypy webserver for serving static contents")

    cherry.set_defaults(func= lambda args: CherryPy.start(webapp))


    global argv
    argv = parser.parse_args()

    # update _config_ from json conf file when required:
    if argv.conffile and _.conffile: 
        with open(_.conffile) as fi:
            _config_.update(json.load(fi))

    # update current settings when required:
    _.verbosity = getattr(argv, "verbosity", _.verbosity)
    _.webapp = getattr(argv, "webapp", _.webapp)

    global mongo_disabled, cherrypy_enabled, multi_threading
    mongo_disabled = getattr(argv, "mongo_disabled", mongo_disabled)
    cherrypy_enabled = getattr(argv, "cherrypy", cherrypy_enabled)
    multi_threading = getattr(argv, "multi_threading", multi_threading)
    
    return argv


def init():
    """ init a new sweetheart project """

    from urllib.parse import urljoin

    # ensure relevant _config_ init:
    #FIXME: allow custom project initialization
    assert _project_ == "sweetheart"

    # start install process:
    print("\n[SWEETHEART] init process is starting now")
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
            #"node-vue",
            "libjs-vue",
            "libjs-highlight.js",
            "libjs-bootstrap4",  
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
            "cherrypy",
            "uvicorn",
            "aiofiles",#NOTE: required with starlette
            "bottle",
            "mistune",
            "mkdocs-material",
            #"openpyxl",
            *_config_["web_framework"].split()
        ])
    print("\nINIT step4: downloading resources...\n")

    os.chdir("/opt/sweetheart/webpages/usual_resources")
    for url in [
        "https://raw.githubusercontent.com/alsacreations/KNACSS/master/css/knacss.css",
        "https://www.w3schools.com/w3css/4/w3.css" ]:
        print("download file:", url)
        subproc.run(["wget","-q","--no-check-certificate",url])

    pcloud = lambda file: urljoin(_config_["cloud_public"], file)

    for file, path in _.copyfiles.items():
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
        fo.write("\n".join((
            "#!/bin/sh",
            "/opt/sweetheart/programs/envPy/bin/python3 -m sweet $*",
        )) )

    subproc.bash("sudo ln --symbolic \
        /opt/sweetheart/programs/scripts/sweet /usr/local/bin/")
    subproc.bash("sudo chmod 777 /usr/local/bin/sweet")

    # start uvicorn webserver allowing multi-threading
    # $ uvicorn sweet:app
    with open("uvicorn","w") as fo:
        fo.write("\n".join((
            f"#!/opt/{_project_}/programs/envPy/bin/python3",
            "from os import chdir",
            "from sys import argv",
            "from uvicorn import run",
            f"chdir({_config_['working_dir']})",
            f"run(argv[1],host='{_.uargs['host']}',port={_.uargs['port']})",
        )) )

    subproc.bash(f"sudo ln --symbolic \
        /opt/{_project_}/programs/scripts/uvicorn /usr/local/bin/")
    subproc.bash("sudo chmod 777 /usr/local/bin/uvicorn")


if __name__ == "__main__":

    # build the Command Line Interface
    # will launch the "init" process if required before modules import
    argv = cli()

    if argv.update_pcloud:
        cloud.update_files()

    if argv.edit_config:
        _.edit()

    if argv.venv:
        subproc.bash(_config_["sh_venv"])
        quit()

    if argv.init:
        init()
        quit()


  #############################################################################
 ########## CHERRYPY FACILITIES ##############################################
#############################################################################

try:
    import cherrypy
    _.cherrypy = True

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


except:
    echo("cherrypy not implemented within current config", mode="stack")
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

#import sklearn
echo("AI not implemented within current config", mode="stack")

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
            <h3>sweetheart</h3>
            <p>a supercharged heart for the non-expert hands</p>
            <p>be aware that you could fall in love with it</p>
            <p><a href="{async_host}/document/welcome" 
                class="btn" role="button">go farer ahead now !</a></p>
            <p><br><br><br><em>this message appears because there
                was nothing else to render here</em></p>
            </div>""")

    template_path = os.path.join(_config_["templates_dir"], source)
    if os.path.isfile(template_path):

        # render html content from given bottle template:
        return HTMLResponse(template(
            template_path,
            **_config_["templates_settings"],
            **kwargs ))

    elif source.endswith(".md") and os.path.isfile(source):

        # render html content from given markdown file:
        with open(source) as file:
            return HTMLResponse(template(
                os.path.join(_config_["templates_dir"],"document.txt"),
                text= markdown(file.read()),
                **_config_["templates_settings"],
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
    os.chdir(_config_["working_dir"])
    echo("set working directory:", os.getcwd())
    
    # then build routing depending of given arguments:
    if isinstance(routes, dict):
        echo("create and route starlette objects from dict")
        for segment,endpoint in routes.items():
            webapp.append( Route(segment,endpoint) )

            verbose("callable segment:",callable(endpoint),"",segment)

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

    if cherrypy_enabled:
        # start cherrypy as external service:
        # this will happen with bash command 'sweet -c start'
        echo("try running cherrypy webserver as external service")
        subproc.service(_config_["sh_cherrypy"])

    # set routing and create Starlette object:
    webapp.mount(route_options=True)

    for i, route in enumerate(webapp):
        verbose(i+1,"  type:", type(route))
        assert isinstance(route,Route) or isinstance(route,Mount)
    
    # auto start the webapp within webbrowser:
    if _.webapp: os.system(_config_["sh_webapp"])

    # at last start the uvicorn webserver:
    if multi_threading:
        #FIXME: only for test
        subproc.service("uvicorn sweet:webapp.star")
    else:
        echo("quickstart: uvicorn multi-threading is not available here")
        uvicorn.run(webapp.star, **_.uargs)


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
    # methodes for main settings: mount() star()

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
    # optional facility for better performances

    @cherrypy.expose
    def default(self):
        return """
        <link rel="stylesheet" href="/resources/knacss.css">
        <div class="txtcenter">
        <h1><br><br>I'm Ready<br><br></h1>
        <h3>cherrypy server is running</h3>
        <p>provide better performances serving static files</p>
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

def mkdocs(working_dir=None):
    """build static documentation from markdown files
    TODO: mkdocs to replace by an integrated sweetheart document generator"""

    # set the current working directory:
    if not working_dir: working_dir=_config_["docs_dir"]
    os.chdir(working_dir)
    echo("set working directory:", os.getcwd())

    # check if mkdocs.yml is existing and create it if not:
    if not os.path.isfile(
        os.path.join(_config_["docs_dir"],"mkdocs.yml")):
        subproc.run([_py3_,"-m","mkdocs","new","."])

    # build static docs website:
    subproc.run([_py3_,"-m","mkdocs","build"])

    # open static docs website:
    if hasattr(argv,"open") and argv.open:
        subproc.bash(_config_["sh_opendocs"])
    

  #############################################################################
 ########## COMMAND LINE & MESSAGES SETUP ####################################
#############################################################################

if __name__ == "__main__":
    
    if not hasattr(argv,"script") \
        and not argv.update_pcloud \
        and not argv.edit_config :

        # inform about current version:
        print("* sweet.py running version:", __version__)
        print("* written by ", __author__)
        print("* shared under CeCILL-C FREE SOFTWARE LICENSE AGREEMENT")

        # provide the available public objects list:
        if _.verbosity:

            objects = dict( (k,v) for k,v in globals().items() \
                if k[0] != "_" and not repr(v).startswith("<module") )

            print("--verbosity  available objects provided by sweet.py:")
            import pprint
            print(); pprint.pprint(objects); print()

        # release stacked messages:
        echo(mode="release")

        # adjust config and settings:
        if cherrypy_enabled and not _.cherrypy:
            cherrypy_enabled = False

        # inform about config status:
        if _.verbosity and _project_ != "sweetheart":
            echo(f"'_config_' built for the '{_project_}' project directory")
            verbose("configuration initialized from PWD:", _dir_)

    # execute dedicated function related to the cli:
    argv.func(argv)
