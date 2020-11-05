"""
provide simple use of highest quality components
for building full-stacked webapps including AI
"""
__version__ = "0.1.0-beta6"
__license__ = "CeCILL-C"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"


# hardcoded default module settings:
ai_enabled = False
mongo_disabled = False
cherrypy_enabled = False
multi_threading = False

# allow setting of 3 webservers respectively for data, statics, mdbook
async_host = "http://127.0.0.1:8000"# uvicorn webserver
static_host = "http://127.0.0.1:8080"# cherrypy webserver
book_host = "http://127.0.0.1:3000"# serve mdbook (rust lib)


# early import:
import os, subprocess, json
from collections import UserList, UserDict

# - main modules import are within the WEBAPP FACILITIES section
# - cherrypy import is within the CHERRYPY FACILITIES section
# - pymongo import is within the subroc.mongod method
# - some modules import from standard libs are within relevant objects

# allow dedicated configs for dev purpose:
_dir_ = os.environ["PWD"].split(os.sep)
if _dir_[1] == "opt" and _dir_[2:]: _project_ = _dir_[2]
else: _project_ = "sweetheart"
_py3_ = f"/opt/{_project_}/programs/envPy/bin/python3"


  #############################################################################
 ########## CONFIGURATION ####################################################
#############################################################################

# provide the default configuration:
# should be updated using _config_.update({ "key": value })
_config_ = {

    ## default json configuration file (hardcoded here):
    "__conffile__": f"/opt/{_project_}/configuration/sweet.json",

    ## webapps settings:
    "working_dir": f"/opt/{_project_}/webpages",
    "description": "build at the speedlight full-stacked webapps including AI",
    "webbook": f"\\\\wsl$\\Ubuntu\\opt\\{_project_}\\webpages\\markdown_book\\index.html",

    "webbrowser": "msedge.exe", # msedge.exe|brave.exe|firefox.exe
    "web_framework": "starlette",# starlette|fastapi
    "ai_modules": "sklearn",# select py3 imports

    "templates_dir": "bottle_templates",
    "templates_settings" : {

        "_default_libs_": "knacss py",
        "_static_": "",# ""=disabled
        "_async_": async_host,
        "_book_": "",# ""=disabled,
    },

    ## set cherrypy default url segments configs:
    "cherrypy": {
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

    "scripts": {

        "python": f"{_py3_}",
        "upload": f"{_py3_} setup.py sdist bdist_wheel && {_py3_} -m twine upload dist/*",
        "remote": "git remote add origin $*",
        "commit": 'git add * && git commit -m "$*" && git push origin master',
        "newbk": "mdbook init $*",
    },

    ## settings for the --init process:
    "apt-install": [

        "python3-venv",
        "rustc",
        "mongodb",
        #"xterm",
        "git",
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
        #"mdbook-mermaid",
    ],
    "pip-install": [

        "sweetheart",
        "pymongo",
        "uvicorn",
        "aiofiles",# required with starlette
        "bottle",
        "setuptools",
        "twine",
        "wheel",
    ],
    "npm-install": [

        "brython",# allow python scripts within html
        "assemblyscript",# Webassembly with Typescript
    ],
    "wget-install-resources": [

        "https://raw.githubusercontent.com/alsacreations/KNACSS/master/css/knacss.css",
        "https://www.w3schools.com/w3css/4/w3.css"
    ],
    ## extra packages install settings:
    "pkg-install": {

        "excel": "pip: openpyxl pandas",
    },
}
class ConfigAccess(UserDict):
    """provide a convenient _config_ accessor tool"""

    # general settings:
    verbose = False
    cherrypy = False
    webapp = False # ENABLE= set url
    mdbook = _config_["templates_settings"].get("_book_")
    winapp = _config_["webbrowser"].endswith(".exe")
    
    locker = 0
    def __init__(self, conffile:str=None):
        """final configuration completion
        allowing json configuration file selection"""
        cls = ConfigAccess
        assert cls.locker == 0; cls.locker = 1

        # top-level config settings:
        cls.conffile= conffile if os.path.isfile(conffile) else None

        # deep config settings:
        self.data = {

        "run": {
            # webbrowsers shell commands:
            "webbrowser": {
                "msedge.exe": f"cmd.exe /c start msedge.exe --app=",
                "brave.exe": f"cmd.exe /c start brave.exe --app=",
                "firefox.exe": f"cmd.exe /c start firefox.exe --app=" },
        },

        # uvicorn arguments dict:
        "uargs": {
            "host": async_host.split(":")[1].strip("/"),
            "port": int(async_host.split(":")[2]),
            "log_level": "info" },

        # data for building new project dir:
        "__basedirs__": """[
            f"/opt/{_project_}",
            f"/opt/{_project_}/configuration",
            f"/opt/{_project_}/database",
            f"/opt/{_project_}/documentation",
            f"/opt/{_project_}/documentation/sweetbook",
            f"/opt/{_project_}/documentation/sweetbook/book",
            f"/opt/{_project_}/documentation/sweetbook/src",
            f"/opt/{_project_}/programs",
            f"/opt/{_project_}/programs/scripts",
            f"/opt/{_project_}/webpages",
            f"/opt/{_project_}/webpages/bottle_templates",
            f"/opt/{_project_}/webpages/markdown_files",
            f"/opt/{_project_}/webpages/markdown_book",
            f"/opt/{_project_}/webpages/usual_resources"
        ]""",
        
        "__copyfiles__": """{
            "cherrypy.conf": f"/opt/{_project_}/configuration",
            "config.xlaunch": f"/opt/{_project_}/configuration",
            "book.toml": f"/opt/{_project_}/documentation/sweetbook",
            "SUMMARY.md": f"/opt/{_project_}/documentation/sweetbook/src",
            "welcome.md": f"/opt/{_project_}/documentation/sweetbook/src",
            "sweet.HTML": f"/opt/{_project_}/webpages",
            "login.txt": f"/opt/{_project_}/webpages/bottle_templates",
            "favicon.ico": f"/opt/{_project_}/webpages/usual_resources",
            "sweetheart-logo.png": f"/opt/{_project_}/webpages/usual_resources",
        }""",
    }

    @property
    def webbrowser(self) -> str:
        select = _config_["webbrowser"]
        return self.data["run"]["webbrowser"][select]
    @property
    def copyfiles(self) -> dict:
        return eval(self.data["__copyfiles__"])
    @property
    def basedirs(self) -> list:
        return eval(self.data["__basedirs__"])
    
    # "key1.key2" -> ["key1"]["key2"]
    ksplit = lambda keys:\
        "".join([f"['{key}']" for key in keys.split(".")])

    def __getitem__(self,keys:str):
        try:
            # look for keys in self.data:
            return eval(f"self.data{ConfigAccess.ksplit(keys)}")
        except:
            # if not, look for keys within _config_:
            verbose("get _config_ item via ConfigAcess:", keys)
            return eval(f"_config_{ConfigAccess.ksplit(keys)}")

    def __setitem__(self,key,val):
        raise NotImplementedError
    
    @classmethod
    def edit(cls):
        """edit _config_ as json configuration file"""
        echo("edit config as json file: %s"%_config_["__conffile__"])
        with open(_config_["__conffile__"],"w") as fo:
            fo.write(json.dumps(_config_, indent=2))
    
    @classmethod
    def update(cls):
        """update _config_ from setted json conffile"""
        assert cls.conffile is not None
        with open(cls.conffile) as fi:
            _config_.update(json.load(fi))


# set the json configuration filename here:
#NOTE: loaded only with '-cf' option given within CLI
_ = ConfigAccess(_config_["__conffile__"])
_deepconfig_ = _.data


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
    """tools for executing linux shell commands"""
    bash = lambda *args,**kwargs: subprocess.run(*args,shell=True,**kwargs)
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
    def exec(cls,args:list):
        """
        execute given script provided by _config_["scripts"]
        it should be called from the command line interface

        - accepts multilines-commands separated by ;
        - arguments can be passed-through using the $* pattern
        - sudo bash commands are forbidden here
        """
        script:str = _config_["scripts"].get(f"{args.script[0]}","")
        if script:
            # stop any 'sudo' cmd given here:
            assert script.find("sudo") == -1

            del args.script[0]
            script = script.replace("$*"," ".join(args.script))
            for cmd in script.split(";"):
                echo("shell$",cmd)
                cls.bash(cmd)
        else:
            echo("sweet.py shell: Error, invalid script name given")

    @classmethod
    def webbrowser(cls,url):
        """open given url in webbrowser defined within _config_"""
        if not url[0] in ["'",'"']: url= f"'{url}'"
        cls.bash( _.webbrowser + url )
    
    @staticmethod
    def wslpath(path):
        """switch a linux path to a wsl path"""
        #FIXME: works only for ubuntu
        return "\\".join(["\\","wsl$","ubuntu",*path.split(os.sep)])

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

    pmount = "sudo mount -t drvfs p: /mnt/p"
    local = "/mnt/p/Public Folder/sweetheart"
    public = "https://filedn.eu/l2gmEvR5C1WbxfsrRYz9Kh4/sweetheart/"
    SwtBookSrc = "/opt/incredible/documentation/sweetbook/book"
    SwtBookDest = local

    @staticmethod
    def update_files():
        #FIXME: dev tool not for users
        echo("updating init files provided from pcloud...")
        if not os.path.isdir(cloud.local): subproc.bash(cloud.pmount)
        for filename, path in _.copyfiles.items():

            source = os.path.join(path, filename)
            dest = cloud.local
            verbose(source, " -> ", dest)
            subproc.run(["cp","-u",source,dest])

        echo("updating sweetbook files...")
        subproc.run(["cp","-R","-u",cloud.SwtBookSrc,cloud.SwtBookDest])

        echo("all updates done to the pcloud drive")

    @staticmethod
    def download(files:dict):
        """downloads files at the right place from a dict
        files= { "filename": "/destination/path/to/file" }"""

        from urllib.parse import urljoin
        src = lambda file: urljoin(cloud.public,file)
        curdir = os.getcwd()

        for file, path in files.items():
            verbose("download file:", src(file))
            os.chdir(path)
            subproc.run(["wget","-q","--no-check-certificate",src(file)])
        
        os.chdir(curdir)


class mdbook:
    """markdown documentation tools using rust/mdBook"""

    @staticmethod
    def start(args):
        """
        Command Line Interface facilities:
        $ sweet book            open default book for the project
        $ sweet book --build    init/build book within current directory
        $ sweet book --open     open book within current directory
        """
        if args.build:
            # init/build book within current directory:
            echo("build mdBook within directory:", os.getcwd())
            mdbook.init(os.getcwd())
            mdbook.build()
        
        if args.open:
            # open book within current directory:
            path = os.path.join(os.getcwd(),"book","index.html")
            if _.winapp: path = subproc.wslpath(path)
            echo("open mdBook at",path)
            mdbook.open(path)

        if not args.build and not args.open:
            # open default book for the project:
            mdbook.open()

    @staticmethod
    def init(directory:str):
        """init a new mdbbok within given directory"""
        # check if a doc is existing and create it if not:
        if not os.path.isfile(os.path.join(directory,"book.toml")):

            #FIXME: input="n" means git features not activated
            subproc.run(["mdbook","init","--force",directory],
                capture_output=True, text=True, input="n")

    @staticmethod
    def build(directory:str=""):
        subproc.run(["mdbook","build",directory])

    @staticmethod
    def open(directory:str=""):
        if not directory: directory = _config_["webbook"]
        subproc.webbrowser(directory)

    @staticmethod
    def serve(directory:str=""):
        if not directory: directory= _config_["working_dir"]
        echo("start the mdbook server (rust)")
        #FIXME: rust toolchain not implemented
        subproc.service(
            f"~/.cargo/bin/mdbook serve {directory}" )


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

        ini.label("set rust toolchain")
        ini.sh(["rustup","update"])
        ini.cargo(_config_["cargo-install"])
        
        ini.label("create directories")
        ini.mkdirs(_.basedirs)

        # directories settings:
        ini.sh(["sudo","chmod","777","-R",f"/opt/{_project_}"])

        ini.ln(["/usr/share/javascript",
            f"/opt/{_project_}/webpages/javascript_libs"])

        ini.ln([f"/opt/{_project_}/documentation/sweetbook/book",
            f"/opt/{_project_}/webpages/sweet_documentation"])

        ini.label("build python3 virtual env")
        ini.sh(["python3","-m","venv",f"/opt/{_project_}/programs/envPy"])
        ini.pip(_config_["pip-install"]+_config_["web_framework"].split())
        if ai_enabled: ini.pip(_config_["ai_modules"].split())

        # *change current working directory:
        os.chdir(f"/opt/{_project_}/webpages")

        toml = """
[book]
multilingual = false
src = "markdown_files"
[build]
build-dir = "markdown_book"
[preprocessor.toc]
command = "mdbook-toc"
renderer = ["html"]
"""
        SUMMARY = """
# Summary
[Welcome](./welcome.md)
"""
        welcome = f"""
# Welcome !
write your documentation in */markdown_files* directory\n
`sweet book --build` for building it\n
`sweet book --open` for open it
"""
        # build documentation setting files:
        ini.label("init project documentation")

        with open("book.toml","w") as fo:
            fo.write(toml.strip())
        with open("markdown_files/SUMMARY.md","w") as fo:
            fo.write(SUMMARY.strip())
        with open("markdown_files/welcome.md","w") as fo:
            fo.write(welcome.strip())

        mdbook.build()

        ini.label("install node modules")
        ini.sh("npm init --yes",shell=True)
        ini.npm(_config_["npm-install"])

        # *change current working directory:
        os.chdir(f"/opt/{_project_}/webpages/usual_resources")

        ini.label("download webapp resources")
        ini.wget(_config_["wget-install-resources"])
        cloud.download(_.copyfiles)

        # build sweetheart documentation:
        mdbook.build(f"/opt/{_project_}/documentation/sweetbook")
        
        # *change current working directory:
        os.chdir(f"/opt/{_project_}/programs/scripts")

        ini.label("build local bash commands")
        ini.locbin("sweet","uvicorn","sws")

        print("\nINIT all done!\n")


    _sweet_ = f"""
#!/bin/sh
{_py3_} -m sweet $*
"""
    _sws_ = f"""
#!/bin/sh
{_py3_} -m sweet shell $*
"""
    _uvicorn_ = f"""
#!{_py3_}
from os import chdir
from sys import argv
from uvicorn import run
chdir("{_config_['working_dir']}")
run(argv[1],host='{_["uargs.host"]}',port={_["uargs.port"]})
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
        for pth in data: 
            verbose(f"mkdir {pth}")
            cls.sh(["sudo","mkdir",pth])
    
    @classmethod
    def wget(cls,data:list):
        # download files using 'wget'
        for url in data:
            verbose(f"download file: {url}")
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
    
    @classmethod
    def install(cls,args):
        """install extra packages defined within ConfigAccess"""

        # *change current working directory:
        #NOTE: mandatory for using ini.npm
        os.chdir(_config_["working_dir"])

        for package in args:
            instrucs:str = _["install"].get(package,"").split(";")
            for cmd in instrucs:
                if cmd.startswith("pip:"): ini.pip(cmd[4:].split())
                elif cmd.startswith("apt:"): ini.apt(cmd[4:].split())
                elif cmd.startswith("cargo:"): ini.cargo(cmd[6:].split())
                elif cmd.startswith("npm:"): ini.npm(cmd[4:].split())


  #############################################################################
 ########## COMMAND LINE INTERFACE ###########################################
#############################################################################

class CommandLine:
    """build Command Line Interface with ease"""

    locker = 0
    def __init__(self):
        cls = CommandLine
        assert cls.locker == 0; cls.locker = 1

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
        help=f"load config from configuration file: {_.conffile}")

    cli.add("-ai","--intelligence",action="store_true",
        help="enable machine learning capabilities (AI)")

    cli.add("--init",action="store_true",
        help="launch init process for building new sweetheart project")

    cli.add("--edit-config",action="store_true",
        help="provide a default configuration json file")

    #FIXME: provisional dev tool:
    cli.add("--update-cloud",action="store_true")


    # create the subparser for the "shell" command:
    cli.sub("shell",help="execute script given by the current config")
    cli.set(subproc.exec)

    cli.add("script",nargs='+',
        help=f'{ "|".join(_config_["scripts"].keys()) }')


    # creat the subparser for the 'book' command:
    cli.sub("book",help="provide full featured documentation from markdown files")
    cli.set(mdbook.start)

    cli.add("-o","--open",action="store_true",
        help="open html documentation within webbrowser")

    cli.add("-b","--build",action="store_true",
        help="build html documentation from markdown files")

    #TODO: add argument for creating new book directory


    # create the subparser for the "start" command:
    cli.sub("start",help="start required services for running webapps")
    cli.set(lambda args: quickstart())

    cli.add("-x","--mongo-disabled",action="store_true",
        help="start without the mongo database server")

    cli.add("-a","--webapp",action="store_true",
        help="start within the webbrowser as an app")

    cli.add("-c","--cherrypy",action="store_true",
        help="start cherrypy as an extra webserver for static contents")

    cli.add("-m","--multi-threading",action="store_true",
        help="start uvicorn webserver allowing multi-threading")


    # create the subparser for the "run-cherrypy" command:
    cli.sub("run-cherrypy",
        help="run cherrypy webserver for serving static contents")
    cli.set(lambda args: CherryPy.start(webapp))


    argv = cli.parse()

    # update _config_ from json conf file when required:
    if argv.conffile: ConfigAccess.update()
        
    # update current settings when required:
    ConfigAccess.verbose = getattr(argv, "verbose", _.verbose)
    ConfigAccess.webapp = async_host \
        if hasattr(argv,"webapp") and argv.webapp else None

    mongo_disabled = getattr(argv, "mongo_disabled", mongo_disabled)
    cherrypy_enabled = getattr(argv, "cherrypy", cherrypy_enabled)
    multi_threading = getattr(argv, "multi_threading", multi_threading)
    ai_enabled = getattr(argv, "machine_learning", ai_enabled)
    
    # start early processes when required:
    if argv.update_cloud: cloud.update_files()
    if argv.edit_config: ConfigAccess.edit()
    if argv.init: ini()


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
    echo("cherrypy not implemented within current config",mode="stack")
    class cherrypy:
        """implement cherrypy.expose as a ghost method"""
        @classmethod
        def expose(*args):
            pass


  #############################################################################
 ##########  BOTTLE TEMPLATING ###############################################
#############################################################################
# MIT Lisence 
# https://github.com/bottlepy/bottle/blob/master/bottle.py

# class BottleException(Exception):
#     """ A base class for exceptions used by bottle. """
#     pass

# class TemplateError(BottleException):
#     pass

# class BaseTemplate(object):
#     """ Base class and minimal API for template adapters """
#     extensions = ['tpl', 'html', 'thtml', 'stpl']
#     settings = {}  #used in prepare()
#     defaults = {}  #used in render()

#     def __init__(self,
#                  source=None,
#                  name=None,
#                  lookup=None,
#                  encoding='utf8', **settings):
#         """ Create a new template.
#         If the source parameter (str or buffer) is missing, the name argument
#         is used to guess a template filename. Subclasses can assume that
#         self.source and/or self.filename are set. Both are strings.
#         The lookup, encoding and settings parameters are stored as instance
#         variables.
#         The lookup parameter stores a list containing directory paths.
#         The encoding parameter should be used to decode byte strings or files.
#         The settings parameter contains a dict for engine-specific settings.
#         """
#         self.name = name
#         self.source = source.read() if hasattr(source, 'read') else source
#         self.filename = source.filename if hasattr(source, 'filename') else None
#         self.lookup = [os.path.abspath(x) for x in lookup] if lookup else []
#         self.encoding = encoding
#         self.settings = self.settings.copy()  # Copy from class variable
#         self.settings.update(settings)  # Apply
#         if not self.source and self.name:
#             self.filename = self.search(self.name, self.lookup)
#             if not self.filename:
#                 raise TemplateError('Template %s not found.' % repr(name))
#         if not self.source and not self.filename:
#             raise TemplateError('No template specified.')
#         self.prepare(**self.settings)

#     @classmethod
#     def search(cls, name, lookup=None):
#         """ Search name in all directories specified in lookup.
#         First without, then with common extensions. Return first hit. """
#         if not lookup:
#             raise depr(0, 12, "Empty template lookup path.", "Configure a template lookup path.")

#         if os.path.isabs(name):
#             raise depr(0, 12, "Use of absolute path for template name.",
#                        "Refer to templates with names or paths relative to the lookup path.")

#         for spath in lookup:
#             spath = os.path.abspath(spath) + os.sep
#             fname = os.path.abspath(os.path.join(spath, name))
#             if not fname.startswith(spath): continue
#             if os.path.isfile(fname): return fname
#             for ext in cls.extensions:
#                 if os.path.isfile('%s.%s' % (fname, ext)):
#                     return '%s.%s' % (fname, ext)

#     @classmethod
#     def global_config(cls, key, *args):
#         """ This reads or sets the global settings stored in class.settings. """
#         if args:
#             cls.settings = cls.settings.copy()  # Make settings local to class
#             cls.settings[key] = args[0]
#         else:
#             return cls.settings[key]

#     def prepare(self, **options):
#         """ Run preparations (parsing, caching, ...).
#         It should be possible to call this again to refresh a template or to
#         update settings.
#         """
#         raise NotImplementedError

#     def render(self, *args, **kwargs):
#         """ Render the template with the specified local variables and return
#         a single byte or unicode string. If it is a byte string, the encoding
#         must match self.encoding. This method must be thread-safe!
#         Local variables may be provided in dictionaries (args)
#         or directly, as keywords (kwargs).
#         """
#         raise NotImplementedError

# class SimpleTemplate(BaseTemplate):
#     def prepare(self,
#                 escape_func=html_escape,
#                 noescape=False,
#                 syntax=None, **ka):
#         self.cache = {}
#         enc = self.encoding
#         self._str = lambda x: touni(x, enc)
#         self._escape = lambda x: escape_func(touni(x, enc))
#         self.syntax = syntax
#         if noescape:
#             self._str, self._escape = self._escape, self._str

#     @cached_property
#     def co(self):
#         return compile(self.code, self.filename or '<string>', 'exec')

#     @cached_property
#     def code(self):
#         source = self.source
#         if not source:
#             with open(self.filename, 'rb') as f:
#                 source = f.read()
#         try:
#             source, encoding = touni(source), 'utf8'
#         except UnicodeError:
#             raise depr(0, 11, 'Unsupported template encodings.', 'Use utf-8 for templates.')
#         parser = StplParser(source, encoding=encoding, syntax=self.syntax)
#         code = parser.translate()
#         self.encoding = parser.encoding
#         return code

#     def _rebase(self, _env, _name=None, **kwargs):
#         _env['_rebase'] = (_name, kwargs)

#     def _include(self, _env, _name=None, **kwargs):
#         env = _env.copy()
#         env.update(kwargs)
#         if _name not in self.cache:
#             self.cache[_name] = self.__class__(name=_name, lookup=self.lookup, syntax=self.syntax)
#         return self.cache[_name].execute(env['_stdout'], env)

#     def execute(self, _stdout, kwargs):
#         env = self.defaults.copy()
#         env.update(kwargs)
#         env.update({
#             '_stdout': _stdout,
#             '_printlist': _stdout.extend,
#             'include': functools.partial(self._include, env),
#             'rebase': functools.partial(self._rebase, env),
#             '_rebase': None,
#             '_str': self._str,
#             '_escape': self._escape,
#             'get': env.get,
#             'setdefault': env.setdefault,
#             'defined': env.__contains__
#         })
#         exec(self.co, env)
#         if env.get('_rebase'):
#             subtpl, rargs = env.pop('_rebase')
#             rargs['base'] = ''.join(_stdout)  #copy stdout
#             del _stdout[:]  # clear stdout
#             return self._include(env, subtpl, **rargs)
#         return env

#     def render(self, *args, **kwargs):
#         """ Render the template using keyword arguments as local variables. """
#         env = {}
#         stdout = []
#         for dictarg in args:
#             env.update(dictarg)
#         env.update(kwargs)
#         self.execute(stdout, env)
#         return ''.join(stdout)


# class StplSyntaxError(TemplateError):
#     pass


# class StplParser(object):
#     """ Parser for stpl templates. """
#     _re_cache = {}  #: Cache for compiled re patterns

#     # This huge pile of voodoo magic splits python code into 8 different tokens.
#     # We use the verbose (?x) regex mode to make this more manageable

#     _re_tok = _re_inl = r'''(
#         [urbURB]*
#         (?:  ''(?!')
#             |""(?!")
#             |'{6}
#             |"{6}
#             |'(?:[^\\']|\\.)+?'
#             |"(?:[^\\"]|\\.)+?"
#             |'{3}(?:[^\\]|\\.|\n)+?'{3}
#             |"{3}(?:[^\\]|\\.|\n)+?"{3}
#         )
#     )'''

#     _re_inl = _re_tok.replace(r'|\n', '')  # We re-use this string pattern later

#     _re_tok += r'''
#         # 2: Comments (until end of line, but not the newline itself)
#         |(\#.*)
#         # 3: Open and close (4) grouping tokens
#         |([\[\{\(])
#         |([\]\}\)])
#         # 5,6: Keywords that start or continue a python block (only start of line)
#         |^([\ \t]*(?:if|for|while|with|try|def|class)\b)
#         |^([\ \t]*(?:elif|else|except|finally)\b)
#         # 7: Our special 'end' keyword (but only if it stands alone)
#         |((?:^|;)[\ \t]*end[\ \t]*(?=(?:%(block_close)s[\ \t]*)?\r?$|;|\#))
#         # 8: A customizable end-of-code-block template token (only end of line)
#         |(%(block_close)s[\ \t]*(?=\r?$))
#         # 9: And finally, a single newline. The 10th token is 'everything else'
#         |(\r?\n)
#     '''

#     # Match the start tokens of code areas in a template
#     _re_split = r'''(?m)^[ \t]*(\\?)((%(line_start)s)|(%(block_start)s))'''
#     # Match inline statements (may contain python strings)
#     _re_inl = r'''%%(inline_start)s((?:%s|[^'"\n])*?)%%(inline_end)s''' % _re_inl

#     # add the flag in front of the regexp to avoid Deprecation warning (see Issue #949)
#     # verbose and dot-matches-newline mode
#     _re_tok = '(?mx)' + _re_tok
#     _re_inl = '(?mx)' + _re_inl


#     default_syntax = '<% %> % {{ }}'

#     def __init__(self, source, syntax=None, encoding='utf8'):
#         self.source, self.encoding = touni(source, encoding), encoding
#         self.set_syntax(syntax or self.default_syntax)
#         self.code_buffer, self.text_buffer = [], []
#         self.lineno, self.offset = 1, 0
#         self.indent, self.indent_mod = 0, 0
#         self.paren_depth = 0

#     def get_syntax(self):
#         """ Tokens as a space separated string (default: <% %> % {{ }}) """
#         return self._syntax

#     def set_syntax(self, syntax):
#         self._syntax = syntax
#         self._tokens = syntax.split()
#         if syntax not in self._re_cache:
#             names = 'block_start block_close line_start inline_start inline_end'
#             etokens = map(re.escape, self._tokens)
#             pattern_vars = dict(zip(names.split(), etokens))
#             patterns = (self._re_split, self._re_tok, self._re_inl)
#             patterns = [re.compile(p % pattern_vars) for p in patterns]
#             self._re_cache[syntax] = patterns
#         self.re_split, self.re_tok, self.re_inl = self._re_cache[syntax]

#     syntax = property(get_syntax, set_syntax)

#     def translate(self):
#         if self.offset: raise RuntimeError('Parser is a one time instance.')
#         while True:
#             m = self.re_split.search(self.source, pos=self.offset)
#             if m:
#                 text = self.source[self.offset:m.start()]
#                 self.text_buffer.append(text)
#                 self.offset = m.end()
#                 if m.group(1):  # Escape syntax
#                     line, sep, _ = self.source[self.offset:].partition('\n')
#                     self.text_buffer.append(self.source[m.start():m.start(1)] +
#                                             m.group(2) + line + sep)
#                     self.offset += len(line + sep)
#                     continue
#                 self.flush_text()
#                 self.offset += self.read_code(self.source[self.offset:],
#                                               multiline=bool(m.group(4)))
#             else:
#                 break
#         self.text_buffer.append(self.source[self.offset:])
#         self.flush_text()
#         return ''.join(self.code_buffer)

#     def read_code(self, pysource, multiline):
#         code_line, comment = '', ''
#         offset = 0
#         while True:
#             m = self.re_tok.search(pysource, pos=offset)
#             if not m:
#                 code_line += pysource[offset:]
#                 offset = len(pysource)
#                 self.write_code(code_line.strip(), comment)
#                 break
#             code_line += pysource[offset:m.start()]
#             offset = m.end()
#             _str, _com, _po, _pc, _blk1, _blk2, _end, _cend, _nl = m.groups()
#             if self.paren_depth > 0 and (_blk1 or _blk2):  # a if b else c
#                 code_line += _blk1 or _blk2
#                 continue
#             if _str:  # Python string
#                 code_line += _str
#             elif _com:  # Python comment (up to EOL)
#                 comment = _com
#                 if multiline and _com.strip().endswith(self._tokens[1]):
#                     multiline = False  # Allow end-of-block in comments
#             elif _po:  # open parenthesis
#                 self.paren_depth += 1
#                 code_line += _po
#             elif _pc:  # close parenthesis
#                 if self.paren_depth > 0:
#                     # we could check for matching parentheses here, but it's
#                     # easier to leave that to python - just check counts
#                     self.paren_depth -= 1
#                 code_line += _pc
#             elif _blk1:  # Start-block keyword (if/for/while/def/try/...)
#                 code_line = _blk1
#                 self.indent += 1
#                 self.indent_mod -= 1
#             elif _blk2:  # Continue-block keyword (else/elif/except/...)
#                 code_line = _blk2
#                 self.indent_mod -= 1
#             elif _cend:  # The end-code-block template token (usually '%>')
#                 if multiline: multiline = False
#                 else: code_line += _cend
#             elif _end:
#                 self.indent -= 1
#                 self.indent_mod += 1
#             else:  # \n
#                 self.write_code(code_line.strip(), comment)
#                 self.lineno += 1
#                 code_line, comment, self.indent_mod = '', '', 0
#                 if not multiline:
#                     break

#         return offset

#     def flush_text(self):
#         text = ''.join(self.text_buffer)
#         del self.text_buffer[:]
#         if not text: return
#         parts, pos, nl = [], 0, '\\\n' + '  ' * self.indent
#         for m in self.re_inl.finditer(text):
#             prefix, pos = text[pos:m.start()], m.end()
#             if prefix:
#                 parts.append(nl.join(map(repr, prefix.splitlines(True))))
#             if prefix.endswith('\n'): parts[-1] += nl
#             parts.append(self.process_inline(m.group(1).strip()))
#         if pos < len(text):
#             prefix = text[pos:]
#             lines = prefix.splitlines(True)
#             if lines[-1].endswith('\\\\\n'): lines[-1] = lines[-1][:-3]
#             elif lines[-1].endswith('\\\\\r\n'): lines[-1] = lines[-1][:-4]
#             parts.append(nl.join(map(repr, lines)))
#         code = '_printlist((%s,))' % ', '.join(parts)
#         self.lineno += code.count('\n') + 1
#         self.write_code(code)

#     @staticmethod
#     def process_inline(chunk):
#         if chunk[0] == '!': return '_str(%s)' % chunk[1:]
#         return '_escape(%s)' % chunk

#     def write_code(self, line, comment=''):
#         code = '  ' * (self.indent + self.indent_mod)
#         code += line.lstrip() + comment + '\n'
#         self.code_buffer.append(code)


# def template(*args, **kwargs):
#     """
#     Get a rendered template as a string iterator.
#     You can use a name, a filename or a template string as first parameter.
#     Template rendering arguments can be passed as dictionaries
#     or directly (as keyword arguments).
#     """
#     tpl = args[0] if args else None
#     for dictarg in args[1:]:
#         kwargs.update(dictarg)
#     adapter = kwargs.pop('template_adapter', SimpleTemplate)
#     lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
#     tplid = (id(lookup), tpl)
#     if tplid not in TEMPLATES or DEBUG:
#         settings = kwargs.pop('template_settings', {})
#         if isinstance(tpl, adapter):
#             TEMPLATES[tplid] = tpl
#             if settings: TEMPLATES[tplid].prepare(**settings)
#         elif "\n" in tpl or "{" in tpl or "%" in tpl or '$' in tpl:
#             TEMPLATES[tplid] = adapter(source=tpl, lookup=lookup, **settings)
#         else:
#             TEMPLATES[tplid] = adapter(name=tpl, lookup=lookup, **settings)
#     if not TEMPLATES[tplid]:
#         abort(500, 'Template (%s) not found' % tpl)
#     return TEMPLATES[tplid].render(kwargs)


  #############################################################################
 ##########  WEBAPP FACILITIES ###############################################
#############################################################################

from bottle import template

import uvicorn
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, FileResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

if ai_enabled: exec(f"import {_config_['ai_modules']}")
else: echo("AI not implemented within current config",mode="stack")

###############################################################################
###############################################################################

# convenient function for rendering html content:
def html(source:str="WELCOME",**kwargs):

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
            <p><a href="documentation/index.html"
                class="btn" role="button">Get Started Now!</a></p>
            <p><br><br><br><em>this message appears because there
                was nothing else to render here</em></p>
            </div>""")

    template_path = os.path.join(_config_["templates_dir"],source)
    if os.path.isfile(template_path):

        # render html content from given bottle template:
        return HTMLResponse(template(
            template_path,
            **_config_["templates_settings"],
            **kwargs ))

    # elif source.endswith(".md") and os.path.isfile(source):

    #     # render html content from given markdown file:
    #     with open(source) as file:
    #         return HTMLResponse(template(
    #             os.path.join(_config_["templates_dir"],"document.txt"),
    #             text= markdown(file.read()),
    #             **_config_["templates_settings"],
    #             **kwargs ))

    elif "</" in source:
        #FIXME: not safe for detecting html content
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
    else: echo("mongoDB client is DISABLED")

    # set mdbook service:
    if _.mdbook: mdbook.serve(_config_["working_dir"])
    else: echo("mdbook server is DISABLED")

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
        webapp.append( Route("/", html("WELCOME")) )

    elif routes is None and isinstance(endpoint, function):
        echo("route a single webpage at", async_host)
        webapp.append( Route("/", routes) )
    else:
        raise ValueError("invalid given arguments")

    if cherrypy_enabled:
        # start cherrypy as external service:
        # this will happen with bash command 'sweet -c start'
        echo("try running cherrypy webserver as external service")
        subproc.service(f"{_py3_} -m sweet run-cherrypy")

    # set routing and create Starlette object:
    webapp.mount(route_options=True)

    for i, route in enumerate(webapp):
        verbose(i+1,"  type:", type(route))
        assert isinstance(route,Route) or isinstance(route,Mount)
    
    # auto start the webapp within webbrowser:
    if _.webapp: subproc.webbrowser(_.webapp)
    
    # at last start the uvicorn webserver:
    if multi_threading:
        #FIXME: only for test
        subproc.service("uvicorn sweet:webapp.star")
    else:
        echo("quickstart: uvicorn multi-threading is not available here")
        uvicorn.run(webapp.star, **_["uargs"])


class WebApp(UserList):

    # default urls endpoints:
    #NOTE: the 'request' argument is required for rendering methods
        
    def index(self, request):
        return html("login.txt")
    
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
            ])
        # mount static resources:
        self.extend([
            Mount("/resources", StaticFiles(directory="usual_resources")),
            Mount("/libs", StaticFiles(directory="javascript_libs")),
            Mount("/modules", StaticFiles(directory="node_modules")),
            Mount("/documentation", StaticFiles(directory="sweet_documentation"))
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


  #############################################################################
 ########## COMMAND LINE & MESSAGES SETUP ####################################
#############################################################################

if __name__ == "__main__":
    
    if not hasattr(argv,"script"):

        # inform about current version:
        verbose("sweet.py running version:", __version__)
        verbose("written by ", __author__)
        verbose("shared under CeCILL-C FREE SOFTWARE LICENSE AGREEMENT\n")

        if _.verbose == 2:

            # provide the available public objects list:
            objects = dict( (k,v) for k,v in globals().items() \
                if k[0] != "_" and not repr(v).startswith("<module") )

            print("**available objects provided by sweet.py:\n")
            import pprint
            pprint.pprint(objects); print()

            # give the current wsl statement:
            print("**current WSL statement:\n")
            subproc.bash("cmd.exe /c 'wsl -l -v'")
            print("")

        # release stacked messages:
        echo(mode="release")

        # force config and settings:
        if not _.cherrypy: cherrypy_enabled = False

        # inform about config status:
        if _.verbose and _project_ != "sweetheart":
            echo(f"config built for the {_dir_[1:3]} project directory")

    # execute dedicated function related to the cli:
    argv.func(argv)
