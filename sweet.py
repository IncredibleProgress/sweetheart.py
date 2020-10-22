"""
provide simple use of highest quality components
for building full-stacked webapps including AI
"""
__version__ = "0.1.0-beta3"
__license__ = "CeCILL-C"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"


# hardcoded default module settings:
AI_enabled = False
mongo_disabled = False
cherrypy_enabled = False
multi_threading = False

# allow setting of 2 webservers respectively for data and statics
async_host = "http://127.0.0.1:8000"# uvicorn webserver
static_host = "http://127.0.0.1:8080"# cherrypy webserver


# early import:
import os, subprocess, json

# - main modules import are within the WEBAPP FACILITIES section
# - cherrypy import is within the CHERRYPY FACILITIES section
# - pymongo import is within the subroc.mongod method
# - some modules import from standard libs are within relevant objects

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

    ## set json configuration file path (hardcoded here):
    "__conffile__": f"/opt/{_project_}/configuration/sweet.json",

    ## webapps settings:
    "working_dir": f"/opt/{_project_}/webpages",
    "docs_dir": f"/opt/{_project_}/documentation",
    
    "ai_modules": "sklearn",# python3 modules
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
\\\\wsl$\\Ubuntu\\opt\\{_project_}\\documentation\\book\\index.html",

    "scripts": {
        "hello": "echo welcome to sweetheart!"
        #"bdist": f"{_py3_} setup.py sdist bdist_wheel",
        #"upload": f"{_py3_} -m twine upload dist/*",
        #"pkgtools": f"{_py3_} -m pip install setuptools twine wheel",
    },
    
    ## --init settings:
    "apt-install": [
        "python3-venv",
        "rustc",
        "mongodb",
        #"xterm",
        #"git",
        "npm",
        "node-typescript",
        #"node-vue",
        "libjs-vue",
        "libjs-bootstrap4",
        "libjs-highlight.js",
    ],
    "cargo-install": [
        "mdbook",
        "mdbook-toc",
    ],
    "pip-install": [
        "sweetheart",
        "pymongo",
        "uvicorn",
        "aiofiles",#NOTE: required with starlette
        "bottle",
        "mistune",
        #"cherrypy",
        #"openpyxl",
    ],
    "npm-install": [
        "brython",
    ],
    "wget-install-resources": [
        "https://raw.githubusercontent.com/alsacreations/KNACSS/master/css/knacss.css",
        "https://www.w3schools.com/w3css/4/w3.css"
    ],

    "__basedirs__": """[
        # given here for ini.__init__()
        f"/opt/{_project_}",
        f"/opt/{_project_}/configuration",
        f"/opt/{_project_}/database",
        f"{_config_['docs_dir']}",
        f"/opt/{_project_}/programs",
        f"/opt/{_project_}/programs/scripts",
        f"/opt/{_project_}/webpages",
        f"/opt/{_project_}/webpages/bottle_templates",
        f"/opt/{_project_}/webpages/markdown_docs",
        f"/opt/{_project_}/webpages/usual_resources"
    ]""",

    ## pcloud settings (for dev purpose):
    "pmount": "sudo mount -t drvfs p: /mnt/p",
    "cloud_local": "/mnt/p/Public Folder/sweetheart",
    "cloud_public": "https://filedn.eu/l2gmEvR5C1WbxfsrRYz9Kh4/sweetheart/",

    "__copyfiles__": """{
        # given here for ini.__init__()
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
    }""",
}

class ConfigAccess:
    """provide a convenient _config_ accessor tool"""
    locker = 0

    # general settings given within CLI:
    verbose = False
    webapp = False
    cherrypy = False

    # uvicorn arguments dict:
    uargs = {
        "host": async_host.split(":")[1].strip("/"),
        "port": int(async_host.split(":")[2]),
        "log_level": "info" }
    
    def __init__(self, conffile:str):
        """allow selection of json configuration file"""
        assert ConfigAccess.locker == 0
        ConfigAccess.locker = 1

        # top-level configuration settings:
        ConfigAccess.conffile=conffile if os.path.isfile(conffile) else None
        ConfigAccess.copyfiles_str = _config_["__copyfiles__"]
        ConfigAccess.basedirs_str = _config_["__basedirs__"]
        # deactivated configuration settings:
        del _config_["__conffile__"]
        del _config_["__copyfiles__"]
        del _config_["__basedirs__"]

    @property
    def copyfiles(self) -> dict:
        return eval(ConfigAccess.copyfiles_str)
    @property
    def basedirs(self) -> list:
        return eval(ConfigAccess.basedirs_str)
    
    def __getitem__(self, keys:str):
        ''' _["key1.key2"] -> _config_["key1"]["key2"] '''
        verbose("get _config_ item via _config_ accessor:", keys)
        ksplit = lambda keys:\
            "".join([f"['{key}']" for key in keys.split(".")])
        return eval( f"_config_{ksplit(keys)}" )
    
    @classmethod
    def edit(cls):
        """edit _config_ as json configuration file"""
        with open(cls.conffile,"w") as fo:
            fo.write(json.dumps(_config_, indent=2))
    
    @classmethod
    def update(cls):
        """update _config_ from setted json conffile"""
        #FIXME: allow custom json config file
        with open(cls.conffile) as fi:
            _config_.update(json.load(fi))


# set the json configuration filename here:
#NOTE: loaded only with '-cf' option given within CLI
_ = CONF = ConfigAccess(_config_["__conffile__"])


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
    if _.verbose: print("|",*args)


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
    def service(cmd:str):
        """select the way for starting external service:
        used for starting mongod, cherrypy, uvicorn within external terminal"""
        
        if _config_["terminal"] == "winterm":
            # start an external service within Windows Terminal
            os.system(f'cmd.exe /c start wt.exe ubuntu.exe run {cmd} &')

        elif _config_["terminal"] == "xterm":
            # start an external service within xterm"""
            os.system("%s xterm -C -geometry 190x19 -e %s &"
                % (_config_["display"], cmd))

        assert _config_["terminal"] in "xterm|winterm"

    @classmethod
    def exec(cls, args):
        cmd = _config_["scripts"][f"{args.script}"]
        echo("exec bash:$", cmd)
        cls.bash(cmd)


    @classmethod
    def mongod(cls):
        """abstract mongoDB settings"""
        global mongoclient, database
        from pymongo import MongoClient
        
        echo("try for getting mongodb client...")
        cls.service('mongod --dbpath="%s"'%_config_["db_path"])

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
    """files management in the cloud"""
    
    @staticmethod
    def update_files():
        #FIXME: dev tool not for users
        echo("updating init files provided from pcloud...")
        for filename, path in _.copyfiles.items():

            source = os.path.join(path, filename)
            dest = _config_["cloud_local"]
            verbose(source, " -> ", dest)

            if not os.path.isdir(_config_["cloud_local"]):
                subproc.bash(_config_["pmount"])

            subproc.run(["cp", source, dest])
        echo("all updates done to the pcloud drive")

    @staticmethod
    def download(files:dict):
        """downloads files at the right place from a dict
        files= { "filename": "/destination/path/to/file" }
        #FIXME: change the current working directory when called"""

        from urllib.parse import urljoin
        src = lambda file: urljoin(_config_["cloud_public"],file)

        for file, path in files.items():
            verbose("download file:", src(file))
            os.chdir(path)
            subproc.run(["wget","-q","--no-check-certificate",src(file)])


class ini:
    """initialize, build, and configure sweetheart
    FIXME: local rust toolchain not implemented"""

    token = 0
    sh = subprocess.run

    def __init__(self, project_name=None):

        global _project_, _py3_
        assert ini.token == 0
        assert _project_ == "sweetheart"

        # set custom project name if given:
        #FIXME: not fully implemented
        if project_name:
            _project_ = project_name
            _py3_ = f"/opt/{_project_}/programs/envPy/bin/python3"

        echo(f"start init process for new project: {_project_}")
        ini.label("install required packages")
        ini.apt(_config_["apt-install"])
        ini.cargo(_config_["cargo-install"])
        
        ini.label("create directories")
        ini.mkdirs(_.basedirs)

        # directories settings:
        ini.sh(["sudo","chmod","777","-R",f"/opt/{_project_}"])
        ini.ln(["/usr/share/javascript",
            f"/opt/{_project_}/webpages/javascript_libs"])

        # build documentation directory:
        #FIXME: '--force' option seems not working
        ini.sh(["mdbook","init","--force",_config_["docs_dir"]])

        ini.label("build python3 virtual env")
        ini.sh(["python3","-m","venv",f"/opt/{_project_}/programs/envPy"])
        ini.pip(_config_["pip-install"]+_config_["web_framework"].split())
        if AI_enabled: ini.pip(_config_["ai_modules"].split())

        # change current working directory:
        os.chdir(f"/opt/{_project_}/webpages")

        ini.label("install node modules")
        ini.sh(["npm","init","--yes"])
        ini.npm(_config_["npm-install"])

        # change current working directory:
        os.chdir(f"/opt/{_project_}/webpages/usual_resources")

        ini.label("download webapp resources")
        ini.wget(_config_["wget-install-resources"])
        cloud.download(_.copyfiles)
        
        # change current working directory:
        os.chdir(f"/opt/{_project_}/programs/scripts")

        ini.label("build local bash commands")
        ini.locbin("sweet","uvicorn")

        print("\nINIT all done!\n")


    _sweet_ = f"""
#!/bin/sh
{_py3_} -m sweet $*
"""

    _uvicorn_ = f"""
#!{_py3_}
from os import chdir
from sys import argv
from uvicorn import run
chdir("{_config_['working_dir']}")
run(argv[1],host='{_.uargs["host"]}',port={_.uargs["port"]})
"""

    @classmethod
    def label(cls,text):
        cls.token += 1
        print(f"\nINIT step{ini.token}: {text}...\n")

    @classmethod
    def apt(cls,data:list):
        # install 'apt' packages 
        cls.sh(["sudo","apt","install"]+data)

    @classmethod
    def cargo(cls,data:list):
        # install 'cargo' packages 
        cls.sh(["cargo","install"]+data)
    
    @classmethod
    def pip(cls,data:list):
        # install 'pip' packages 
        cls.sh([_py3_,"-m","pip","install"]+data)
    
    @classmethod
    def npm(cls,data:list):
        # install 'npm' packages 
        cls.sh(["npm","install"]+data)
        
    @classmethod
    def mkdirs(cls,data:list):
        for pth in data: cls.sh(["sudo","mkdir",pth])
    
    @classmethod
    def wget(cls,data:list):
        # download files using 'wget'
        for url in data:
            
            cls.sh(["wget","-q","--no-check-certificate",url])
    
    @classmethod
    def ln(cls,data:list):
        cls.sh(["sudo","ln","--symbolic"]+data)

    @classmethod
    def locbin(cls,*args:str):

        for scriptname in args:
            assert hasattr(ini,f"_{scriptname}_")

            # create 'scriptname' in the current working dir:
            with open(scriptname,"w") as fo:
                verbose(f"write new script: {scriptname}")
                fo.write(eval(f"ini._{scriptname}_").strip())

            cls.ln([
                f"/opt/{_project_}/programs/scripts/{scriptname}",
                "/usr/local/bin/" ])

            cls.sh(["sudo","chmod","777",f"/usr/local/bin/{scriptname}"])


  #############################################################################
 ########## COMMAND LINE INTERFACE ###########################################
#############################################################################

class CommandLine:
    """build Command Line Interface with ease"""
    locker = 0

    def __init__(self):
        cls = CommandLine

        assert cls.locker == 0
        cls.locker = 1

        import argparse
        cls.parser= argparse.ArgumentParser()
        cls.subparser= cls.parser.add_subparsers()
        cls.dict= { "_": cls.parser }; cls.cur= "_"

        cls.set(lambda args:\
            print("use the '--help' or '-h' option for getting some help"))

        cls.add("-v","--verbose",action="count",
            help="get additional messages about on-going process")
    
    @classmethod
    def add(cls,*args,**kwargs):
        cls.dict[cls.cur].add_argument(*args,**kwargs)

    @classmethod
    def sub(cls,*args,**kwargs):
        cls.cur = args[0]
        cls.dict[args[0]]=cls.subparser.add_parser(*args,**kwargs)
    
    @classmethod
    def set(cls, func):
        cls.dict[cls.cur].set_defaults(func=func)

    @classmethod
    def parse(cls):
        return cls.parser.parse_args()


if __name__ == "__main__":

    # build the Command Line Interface
    # will launch here early processes before modules import
    cli = CommandLine()

    cli.add("-cf","--conffile",action="store_true",
        help="load config from the 'sweet.json' configuration file")

    cli.add("-ai","--machine-learning",action="store_true",
        help="enable machine learning capabilities(AI)")
        
    cli.add("-py","--python-venv",action="store_true",
        help="execute python3 in virtual env built for sweetheart")

    cli.add("--init",action="store_true",
        help="launch init process for building new sweetheart project")

    cli.add("--edit-config",action="store_true",
        help="provide a default configuration json file")

    #FIXME: provisional dev tool:
    cli.add("--update-pcloud",action="store_true")


    # create the parser for the "sh" command:
    cli.sub("sh",help="execute script given by the current config")
    cli.set(subproc.exec)

    cli.add("script",help=f'name of a script given in _config_:\
        {[i for i in _config_["scripts"].keys()]}')


    # set the subparser for the 'book' command:
    cli.sub("book",help="provide nice documentation from markdown files")
    cli.set(lambda args: mdbook())

    cli.add("-o","--open",action="store_true",
        help="open documentation within webbrowser")

    cli.add("-b","--build",action="store_true",
        help="build html documentation from markdown files")


    # create the parser for the "cli" command:
    cli.sub("cli",help="cli required services for running webapps")
    cli.set(lambda args: quickstart())

    cli.add("-x","--mongo-disabled",action="store_true",
        help="cli without the mongo database server")

    cli.add("-a","--webapp",action="store_true",
        help="cli within the webbrowser as an app")

    cli.add("-c","--cherrypy",action="store_true",
        help="cli cherrypy as an extra webserver for static contents")

    cli.add("-m","--multi-threading",action="store_true",
        help="cli uvicorn webserver allowing multi-threading")


    # create the parser for the "run-cherrypy" command:
    cli.sub("run-cherrypy",
        help="run cherrypy webserver for serving static contents")
    cli.set(lambda args: CherryPy.cli(webapp))


    argv = cli.parse()

    # update _config_ from json conf file when required:
    if argv.conffile: ConfigAccess.update()
        
    # update current settings when required:
    ConfigAccess.verbose = getattr(argv, "verbose", _.verbose)
    ConfigAccess.webapp = getattr(argv, "webapp", _.webapp)

    mongo_disabled = getattr(argv, "mongo_disabled", mongo_disabled)
    cherrypy_enabled = getattr(argv, "cherrypy", cherrypy_enabled)
    multi_threading = getattr(argv, "multi_threading", multi_threading)
    AI_enabled = getattr(argv, "machine_learning", AI_enabled)
    
    # start early processes when required:
    if argv.update_pcloud: cloud.update_files()
    if argv.edit_config: ConfigAccess.edit()
    if argv.init: ini()

    # start standalone action when required:
    if argv.python_venv:
        subproc.bash(_config_["sh_venv"])
        quit()


  #############################################################################
 ########## CHERRYPY FACILITIES ##############################################
#############################################################################

try:
    import cherrypy
    ConfigAccess.cherrypy = True

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

if not AI_enabled:
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


# convenient function for starting webapp
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

def mdbook(working_dir=None):
    """build static documentation from markdown files"""

    # set the current working directory:
    if not working_dir: working_dir=_config_["docs_dir"]
    os.chdir(working_dir)
    echo("set working directory:", os.getcwd())

    # check if a doc is existing and create it if not:
    if not os.path.isfile(os.path.join(working_dir,"book.toml")):
        subproc.run(["mdbook","init"])

    # build static docs website:
    subproc.run(["mdbook","build"])

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
        verbose("sweet.py running version:", __version__)
        verbose("written by ", __author__)
        verbose("shared under CeCILL-C FREE SOFTWARE LICENSE AGREEMENT")

        # provide the available public objects list:
        if _.verbose == 2:

            objects = dict( (k,v) for k,v in globals().items() \
                if k[0] != "_" and not repr(v).startswith("<module") )

            print("\navailable objects provided by sweet.py:\n")
            import pprint
            pprint.pprint(objects); print()

        # release stacked messages:
        echo(mode="release")
        echo("NEW: make nice docs at the speedlight with rust/mdbook")

        # force config and settings:
        if not _.cherrypy: cherrypy_enabled = False

        # inform about config status:
        if _.verbose and _project_ != "sweetheart":
            echo(f"config built for the {_dir_} project directory")

    # execute dedicated function related to the cli:
    argv.func(argv)
