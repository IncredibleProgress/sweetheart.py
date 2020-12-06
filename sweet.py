"""
provide simple use of highest quality components
for building full-stacked webapps including AI
"""
__version__ = "0.1.0-beta11"
__license__ = "CeCILL-C FREE SOFTWARE LICENSE AGREEMENT"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"


# hardcoded default module settings:
mongo_disabled = False
cherrypy_enabled = False
multi_threading = False

# allow setting of 3 webservers respectively for data, statics, mdbook
async_host = "http://127.0.0.1:8000"# uvicorn webserver
static_host = "http://127.0.0.1:8080"# cherrypy webserver
book_host = "http://127.0.0.1:3000"# serve mdbook (rust crate)
jupyter_host = "http://localhost:8888" # jupyterlab server


import os, sys, subprocess, json
from collections import UserList, UserDict

# - main modules import are within the WEBAPP FACILITIES section
# - cherrypy import is within the CHERRYPY FACILITIES section
# - pymongo import is within the MongoDB.set_client method
# - uvicorn import is within the Uvicorn.run_local method
# - imports from standard libs are included within relevant objects


# provide convenient functions for givin messages
_msg_ = []
def echo(*args, mode="default"):
    """convenient function for printing messages
    mode = 0|default|stack|release"""

    if "_config_" in globals(): label = _config_["echolabel"]
    else: label = _project_

    if mode.lower() == "stack" or mode == 0:
        global _msg_
        _msg_.append(" ".join(args))

    elif mode.lower() == "release":
        for msg in _msg_:
            print("[%s]"% label.upper(),msg)
        _msg_ = []

    elif mode.lower() == "exit":
        print("[%s]"% label.upper(),*args)
        sys.exit()

    else:
        print("[%s]"% label.upper(),*args)

def verbose(*args):
    """convenient function for verbose messages"""
    if _.verbose: print("..",*args)


# allow dedicated configs for custom projects:
_dir_ :list = os.environ["PWD"].split(os.sep)
_swt_ :str = os.path.join(os.getenv("HOME",""),".sweet")

if "-p" in sys.argv: _project_ = sys.argv[sys.argv.index("-p")+1]
elif _dir_[1] == "opt" and _dir_[2:]: _project_ = _dir_[2]
#FIXME: disabled option
#elif os.getenv("SWEET_PROJECT"): _project_ = os.getenv("SWEET_PROJECT")

elif os.path.isfile(_swt_):
    with open(_swt_) as fi: _project_ = fi.readline().strip()
    echo("'.sweet' file read within /home directory")

else: _project_ = "sweetheart"


  #############################################################################
 ########## CONFIGURATION ####################################################
#############################################################################

# provide the default configuration:
# should be updated using _config_.update({ "key": value })
def init_config(values:dict={},project:str=None,):
    """allow you to reset the configuration
    can be usefull importing sweet within Jupyter notebook"""
    global _config_, _py3_, _project_

    if project: _project_ = project
    elif values.get("_project_"): _project_ = values["_project_"]
    _py3_ = f"/opt/{_project_}/programs/sweetenv.py/bin/python3"
    _config_ = {

    ## default json configuration file (hardcoded here):
    "__conffile__": f"/opt/{_project_}/configuration/sweet.json",

    ## webapps settings:
    "working_dir": f"/opt/{_project_}/webpages",
    "description": "sweetheart helps you getting coding full power",

    "webbrowser": "app:msedge.exe", # msedge.exe|brave.exe|firefox
    "webbook": f"/opt/{_project_}/webpages/markdown_book/index.html",
    "notebook_dir": f"/opt/{_project_}/documentation/notebooks",

    "templates_dir": "bottle_templates",
    "templates_settings" : {

        "_default_libs_": "knacss py",
        "_static_": "",# ""=disabled
        "_async_": async_host,
        "_book_": "",# ""=disabled,
    },
    "static_dirs": {

        "/resources": "usual_resources",
        "/libs": "javascript_libs",
        "/modules": "node_modules",
        "/documentation": "sweet_documentation",
    },
    "static_files": {

        "favicon": "usual_resources/favicon.ico",
    },
    ## set cherrypy default url segments configs:
    "cherrypy": {
        "/": f"/opt/{_project_}/configuration/cherrypy.conf",
    },
    ## database settings:
    "db_host": "localhost",# "localhost" start mongod locally
    "db_port": 27017,
    "db_path": f"/opt/{_project_}/database",
    "db_select": "demo",

    ## bash settings:
    "echolabel": _project_,
    "display": "DISPLAY=:0",
    "terminal": "wsl",# xterm|winterm|wsl
    "gitignore": "y",# y|n

    ## select python3 asgi webframework:
    "web_framework": "starlette",# starlette|fastapi

    ## basic config settings for the --init process:
    "apt-install": [

        "rustc",
        "mongodb",
        "xterm",
        "npm",
        "node-typescript",
        "libjs-bootstrap4",
        "libjs-highlight.js",
        "libjs-vue",
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
        "jupyterlab",
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
    #$ sweet install all -> for installing all within "pkg-install"
    #$ sweet install options -> for installing given "pkg-options"
    "pkg-install": {

        "excel": "pip: xlrd xlwt pyxlsb openpyxl xlsxwriter",
        "science": "apt: fish; pip:scipy tabulate pandas seaborn scikit-learn[alldeps]",
        "pypack": "apt: git; pip: setuptools twine wheel pytest",
        "html": "pip: beautifulsoup4 html5lib lxml",
        "servers": "pip: cherrypy",
    },
    "pkg-options": "pypack science excel html",

    ## set python3 extra modules imports:
    "py-imports": {
        # "module": "", will import the module itself
        "bottle": "template", # bottle|jinja2|mako
        "mistune": "markdown",# jupyterlab dependency
        "sys": "exit",
    },
    ## custom bash commands called by sws
    "scripts": {
        #bash -> sws <command>
        #cmd -> wsl sws <command>
        "python": f"/opt/{_project_}/programs/sweetenv.py/bin/ipython3",
        "setup": f"{_py3_} setup.py install",
        "upload": f"rm -rf dist;{_py3_} setup.py sdist bdist_wheel && {_py3_} -m twine upload dist/*",
        "remote": "git remote add origin $*",
        "commit": 'git add * && git commit -m "$*" && git push origin master',
        "notebook": "sweet run-jupyter --notebook",
        "jupyter":  f"sweet run-jupyter --set-kernel --lab",
        "rmkern": "jupyter kernelspec list && jupyter kernelspec uninstall $*",
        "wsl1": "cmd.exe /c 'wsl --set-default-version 1'",
        "start": "sweet start --mongo-disabled --jupyter --webapp",
        "help": "sweet book sweetbook",
    },
    }; _config_.update(values)

    if ConfigAccess.locker == 1: 
        # autoset config parameters
        global multi_threading, mongo_disabled
        mongo_disabled = True
        multi_threading = True
        # reset the existing backend facilities
        set_backend()
        echo(f"backend objects re-loaded")


class ConfigAccess(UserDict):
    """provide a convenient _config_ accessor tool
    allow json configuration file selection"""

    # command line settings
    verbose = False
    webapp = False
    jupyter = False
    # set trackers
    cherrypy = False
    locker = 0

    def __init__(self,values:dict={}):

        # top-level settings
        init_config(values)
        file = _config_.get("__conffile__","")
        self.conffile= file if os.path.isfile(file) else None

        # allow only one instance of ConfigAccess
        assert ConfigAccess.locker == 0
        ConfigAccess.locker = 1

        # app settings
        self.mdbook = _config_["templates_settings"].get("_book_")
        self.winapp = _config_["webbrowser"].endswith(".exe")

        # deep config settings
        self.data = {
        "force-apt-install": [
            "python3-venv",
        ],
        "force-pip-install": [
            "aiofiles",# required with starlette
            "wheel",# required installing jupyter
        ],
        "run-webbrowser": {                
            # start cmd for usual linux webbrowsers:
            "*": f"{_py3_} -m webbrowser -t",
            "firefox": "firefox",

            # start cmd for usual windows webbrowsers:
            "msedge.exe": "cmd.exe /c start msedge",# windows
            "brave.exe": "cmd.exe /c start brave",
            "app:msedge.exe": "cmd.exe /c start msedge --app=",
            "app:brave.exe": "cmd.exe /c start brave --app=",
        },
        # path to rust crates/cargo command line tools
        "rust-crates": f"{os.environ['HOME']}/.cargo/bin",
        
        # data for building new project dir:
        "__basedirs__": lambda: [
            f"/opt/{_project_}",
            f"/opt/{_project_}/configuration",
            f"/opt/{_project_}/database",
            f"/opt/{_project_}/documentation",
            f"/opt/{_project_}/documentation/notebooks",
            f"/opt/{_project_}/documentation/sweetbook",
            f"/opt/{_project_}/documentation/sweetbook/book",
            f"/opt/{_project_}/documentation/sweetbook/src",
            f"/opt/{_project_}/programs",
            f"/opt/{_project_}/programs/scripts",
            f"/opt/{_project_}/webpages",
            f"/opt/{_project_}/webpages/{_['templates_dir']}",
            f"/opt/{_project_}/webpages/markdown_files",
            f"/opt/{_project_}/webpages/markdown_book",
            f"/opt/{_project_}/webpages/usual_resources"
        ],
        "__copyfiles__": lambda: {
            "cherrypy.conf": f"/opt/{_project_}/configuration",
            "config.xlaunch": f"/opt/{_project_}/configuration",
            "book.toml": f"/opt/{_project_}/documentation/sweetbook",
            "SUMMARY.md": f"/opt/{_project_}/documentation/sweetbook/src",
            "welcome.md": f"/opt/{_project_}/documentation/sweetbook/src",
            "sweet.HTML": f"/opt/{_project_}/webpages",
            "login.txt": f"/opt/{_project_}/webpages/{_['templates_dir']}",
            "favicon.ico": f"/opt/{_project_}/webpages/usual_resources",
            "sweetheart-logo.png": f"/opt/{_project_}/webpages/usual_resources",
        },
        }

    @property
    def copyfiles(self) -> dict:
        return self.data["__copyfiles__"]()
    @property
    def basedirs(self) -> list:
        return self.data["__basedirs__"]()
    
    # "key1.key2" -> ["key1"]["key2"]
    ksplit = lambda keys:\
        "".join([f"['{key}']" for key in keys.split(".")])

    def __getitem__(self,keys:str):
        """get any config items providing a verbose message"""
        try:
            # first look for keys in self.data:
            return eval(f"self.data{ConfigAccess.ksplit(keys)}")
        except:
            # if not look for keys within _config_:
            verbose(f"GET '{keys}' from current config")
            return eval(f"_config_{ConfigAccess.ksplit(keys)}")

    def __setitem__(self,key,val):
        raise NotImplementedError
    
    def edit(self):
        """edit _config_ as json configuration file"""
        echo("edit config as json file: %s"%_config_["__conffile__"])
        with open(_config_["__conffile__"],"w") as fo:
            fo.write(json.dumps(_config_, indent=2))
    
    def update(self):
        """update _config_ from setted json conffile"""
        assert self.conffile is not None
        with open(self.conffile) as fi:
            _config_.update(json.load(fi))


# set the json configuration filename here
#NOTE: loaded only with '-c' option given within CLI
_ = ConfigAccess()
_deepconfig_ = _.data


# adjust parameters for wsl/linux
if os.getenv("WINDIR"):
    raise NotImplementedError

if os.getenv("WSL_DISTRO_NAME") is None:
    echo("NO WSL: set native services for linux")
    _config_["terminal"] = "xterm"
    if _.winapp:
        _.winapp = False
        _config_["webbrowser"] = "*"

elif _.winapp and os.environ["WSL_DISTRO_NAME"] != "Ubuntu":
    echo("WARNING: WSL is not running with Ubuntu")
    _.verbose = True


def set_backend():
    """load or reload provided backend features"""
    global _mongo_,mongoclient,database,jupyter,uvicorn,mdbook

    # set default mongo client and database
    _mongo_ = MongoDB(
        host= _config_["db_host"],
        port= _config_["db_port"])

    mongoclient = _mongo_.client
    database = _mongo_.database

    # set default jupyterlab config
    jupyter = JupyterLab(url=jupyter_host)
    # set default uvicorn config
    uvicorn = Uvicorn(url=async_host)
    # set default mdbook config
    mdbook = MdBook(url=book_host)


  #############################################################################
 ########## SCRIPTS ##########################################################
#############################################################################
_deepconfig_.update({

"$sweet": lambda: f"""
#!/bin/bash
#cd /opt/{_project_}
{_py3_} -m sweet $*
""",

"$sws": lambda: f"""
#!/bin/bash
{_py3_} -m sweet shell $*
""",

"$uvicorn": lambda: f"""
#!{_py3_}
from os import chdir
from sys import argv
from uvicorn import run
chdir("{_config_['working_dir']}")
run(argv[1],host='{uvicorn.host}',port={uvicorn.port})
""",

"book.toml": """
[book]
multilingual = false
src = "markdown_files"
[build]
build-dir = "markdown_book"
[preprocessor.toc]
command = "mdbook-toc"
renderer = ["html"]
""",

"SUMMARY.md": """
# Summary\n
[Welcome](./welcome.md)
""",

"welcome.md": """
# Welcome !\n
build incredible documentation writing files in the *markdown_files* directory\n\n
`sweet book --build` for building it\n\n
`sweet book --open` for open it
""",
})

  #############################################################################
 ########## EXTERNAL SERVICES FACILITIES #####################################
#############################################################################

def shell(args):
    """execute a given script provided by _config_["scripts"]
    it should be called from the command line interface
     - accepts multilines-commands separated by ;
     - arguments can be passed-through using the $* pattern
     - sudo bash commands are forbidden here
    """
    script:str = _config_["scripts"].get(f"{args.script[0]}","")
    if script:
        # stop any 'sudo' cmd given here:
        assert not "sudo" in script
        assert not "su " in script

        del args.script[0]
        script = script.replace("$*"," ".join(args.script))
        for cmd in script.split(";"):
            echo("shell$",cmd.strip())
            subprocess.run(cmd,shell=True)
    else:
        echo("sweet.py shell: Error, invalid script name given")

def winpath(path:str):
    """switch a linux path to a windows path"""
    distro = os.environ['WSL_DISTRO_NAME']
    if path[0] == os.sep:
        return "\\".join(["\\","wsl$",distro,*path.split(os.sep)[1:]])
    elif path.startswith("http"): return path
    else: raise NotImplementedError

def webbrowser(url,select=None):
        """
        open the given url in selected webbrowser within
        '_config_["webbrowser"]' or defined with 'run' if given
        """
        # build bash command:
        if not select: select= _config_["webbrowser"]
        cmd= _deepconfig_["run-webbrowser"][select]
        if not cmd.endswith("=") and not cmd.endswith(" "): cmd+=" "

        # open the given url:
        if _.winapp: url = winpath(url)
        if not url[0] in ["'",'"']: url= f"'{url}'"
        subprocess.run(cmd+url+" &",shell=True)


class SwServer:
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
            os.system(f'cmd.exe /c start wsl {cmd} &')

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


class MongoDB(SwServer):

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


class JupyterLab(SwServer):

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


class Uvicorn(SwServer):

    def __init__(self,*args,**kwargs):
        super(Uvicorn,self).__init__(*args,**kwargs)
        self.app = "sweet:webapp.star"

        # set uvicorn arguments dict
        self.uargs = {
            "host": self.host,
            "port": self.port,
            "log_level": "info" }

    def run_local(self,app,service=None):
        """run the uvicorn webserver
        app argument can be 'str' or 'Starlette' object"""
        if service is None:
            service = multi_threading
        if service is True:
            #FIXME: not fully implemented
            self.service(f"uvicorn {self.app}")
        elif service is False:
            import uvicorn
            uvicorn.run(app,**self.uargs)
        else: raise TypeError


class MdBook(SwServer):
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


class cloud:
    """files management in the cloud"""

    pmount = "sudo mount -t drvfs p: /mnt/p"
    local = "/mnt/p/Public Folder/sweetheart"
    public = "https://filedn.eu/l2gmEvR5C1WbxfsrRYz9Kh4/sweetheart/"
    swBookSrc = "/opt/incredible/documentation/sweetbook/book"

    @staticmethod
    def update_files():
        #FIXME: dev tool not for users
        if not os.path.isdir(cloud.local):
            subprocess.run(cloud.pmount,shell=True)
        for filename, path in _.copyfiles.items():
            source = os.path.join(path, filename)
            dest = cloud.local
            verbose("copy:",source," -> ", dest)
            subprocess.run(["cp","-u",source,dest])

        subprocess.run(["cp","-R","-u",cloud.swBookSrc,cloud.local])
        echo("copy or update files in the cloud done")

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
            subprocess.run(["wget","-q","--no-check-certificate",src(file)])
        
        os.chdir(curdir)


class ini:
    """initialize, build, and configure sweetheart"""

    token = 0
    sh = subprocess.run

    def __init__(self,args):

        global _project_, _py3_
        assert ini.token == 0

        #FIXME: written for transitional purpose
        if hasattr("args","project") and args.project:
            assert _project_ == args.project
            _py3_ = f"/opt/{_project_}/programs/sweetenv.py/bin/python3"
        # any 'incredible' project is forbidden here
        assert _project_ != "incredible"

        echo(f"start init process for new project: {_project_}")
        ini.label("install required packages")
        ini.apt(_deepconfig_["force-apt-install"])
        ini.apt(_config_["apt-install"])

        ini.label("set rust toolchain")
        ini.PATH(_deepconfig_["rust-crates"])
        try:
            ini.sh(["rustup","update"])
            ini.cargo(_config_["cargo-install"])
        except:
            verbose("Error, cargo install failed")
        
        ini.label("create directories")
        ini.mkdirs(_.basedirs)

        # directories settings
        ini.sh(["sudo","chmod","777","-R",f"/opt/{_project_}"])

        ini.ln(["/usr/share/javascript",
            f"/opt/{_project_}/webpages/javascript_libs"])

        ini.ln([f"/opt/{_project_}/documentation/sweetbook/book",
            f"/opt/{_project_}/webpages/sweet_documentation"])
            
        ini.label("build python3 virtual env")
        ini.sh(["python3","-m","venv",f"/opt/{_project_}/programs/sweetenv.py"])
        ini.pip(_deepconfig_["force-pip-install"])
        ini.pip(_config_["pip-install"]+_config_["web_framework"].split())

        #FIXME: following standard libs list given for python 3.8
        stdlibs = ['__future__', '__main__', '_abc', '_ast', '_asyncio', '_bisect', '_blake2', '_bootlocale', '_bz2', '_codecs', '_codecs_cn', '_codecs_hk', '_codecs_iso2022', '_codecs_jp', '_codecs_kr', '_codecs_tw', '_collections', '_collections_abc', '_compat_pickle', '_compression', '_contextvars', '_crypt', '_csv', '_ctypes', '_ctypes_test', '_curses', '_curses_panel', '_datetime', '_dbm', '_decimal', '_dummy_thread', '_elementtree', '_frozen_importlib', '_frozen_importlib_external', '_functools', '_gdbm', '_hashlib', '_heapq', '_imp', '_io', '_json', '_locale', '_lsprof', '_lzma', '_markupbase', '_md5', '_multibytecodec', '_multiprocessing', '_opcode', '_operator', '_osx_support', '_pickle', '_posixshmem', '_posixsubprocess', '_py_abc', '_pydecimal', '_pyio', '_queue', '_random', '_sha1', '_sha256', '_sha3', '_sha512', '_signal', '_sitebuiltins', '_socket', '_sqlite3', '_sre', '_ssl', '_stat', '_statistics', '_string', '_strptime', '_struct', '_symtable', '_testbuffer', '_testcapi', '_testimportmultiple', '_testinternalcapi', '_testmultiphase', '_thread', '_threading_local', '_tkinter', '_tracemalloc', '_uuid', '_warnings', '_weakref', '_weakrefset', '_xxsubinterpreters', '_xxtestfuzz', 'abc', 'aifc', 'antigravity', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2', 'cProfile', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils', 'doctest', 'dummy_threading', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools', 'gc', 'genericpath', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'idlelib', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'ntpath', 'nturl2path', 'numbers', 'opcode', 'operator', 'optparse', 'os', 'ossaudiodev', 'parser', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 'posixpath', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'pydoc_data', 'pyexpat', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3', 'sre_compile', 'sre_constants', 'sre_parse', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'this', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'xxlimited', 'xxsubtype', 'zipapp', 'zipfile', 'zipimport', 'zlib']

        # install modules from py-imports when not a standard libs
        for module in _config_["py-imports"].keys():
            if module.split(".")[0] in stdlibs: continue
            ini.pip([module])

        # set sweetenv.py ipykernel for running jupyter
        jupyter.set_ipykernel()

        # set now a password for running jupyter server
        print("\nWARNING: This is required to set a password for the Jupyter server")
        print("press [RETURN] directly for setting no password (but not recommended)")
        jupyter.set_password()

        # *change current working directory
        os.chdir(f"/opt/{_project_}/webpages")

        # build documentation setting files
        ini.label("init project documentation")

        with open("book.toml","w") as fo:
            fo.write(_deepconfig_["book.toml"].strip())
        with open("markdown_files/SUMMARY.md","w") as fo:
            fo.write(_deepconfig_["SUMMARY.md"].strip())
        with open("markdown_files/welcome.md","w") as fo:
            fo.write(_deepconfig_["welcome.md"].strip())

        try: 
            mdbook.build()
        except:
            verbose("Error, mdbook build failed")
        try:
            ini.label("install node modules")
            ini.sh("npm init --yes",shell=True)
            ini.npm(_config_["npm-install"])
        except:
            verbose("Error, npm install failed")

        # *change current working directory
        os.chdir(f"/opt/{_project_}/webpages/usual_resources")

        ini.label("download webapp resources")
        ini.wget(_config_["wget-install-resources"])
        cloud.download(_.copyfiles)

        # build sweetheart documentation
        mdbook.build(f"/opt/{_project_}/documentation/sweetbook")
        
        # *change current working directory
        os.chdir(f"/opt/{_project_}/programs/scripts")

        ini.label("build local bash commands")
        ini.locbin("sweet","uvicorn","sws")

        print("\nSWEET_INIT all done!\n")

    @classmethod
    def label(cls,text):
        cls.token += 1
        print(f"\nSWEET_INIT_step{ini.token}: {text}\n")

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
            cls.sh(["wget","-nv","-nc","--no-hsts","--no-check-certificate",url])
    
    @classmethod
    def ln(cls,data:list):
        cls.sh(["sudo","ln","--symbolic"]+data)

    @classmethod
    def locbin(cls,*args:str):

        for scriptname in args:
            assert _deepconfig_.get(f"${scriptname}")

            # create 'scriptname' in the current working dir:
            with open(scriptname,"w") as fo:
                verbose(f"write new script: {scriptname}")
                fo.write(_deepconfig_[f"${scriptname}"]().strip())

            cls.ln([
                f"/opt/{_project_}/programs/scripts/{scriptname}",
                "/usr/local/bin/" ])

            cls.sh(["sudo","chmod","777",f"/usr/local/bin/{scriptname}"])
    
    @classmethod
    def install(cls,args):
        """install extra packages defined within ConfigAccess
        two accepted special values: all|options"""

        # *change current working directory:
        #NOTE: needed for using ini.npm
        os.chdir(_config_["working_dir"])

        if "all" in args.packages:
            # install all given packages listed
            args.packages= _config_["pkg-install"].keys()
        elif "options" in args.packages:
            args.packages= [i for i in args.packages if i != "options"]
            args.packages.extend(_config_["pkg-options"].split())
        
        for package in args.packages:
            #FIXME: works only with CLI arguments
            instrucs = _["pkg-install"][package].split(";")
            for cmd in instrucs:
                cmd = cmd.strip()
                ini.label(f"install new packages using {cmd}")
                if cmd.startswith("pip:"): ini.pip(cmd[4:].split())
                elif cmd.startswith("apt:"): ini.apt(cmd[4:].split())
                elif cmd.startswith("cargo:"): ini.cargo(cmd[6:].split())
                elif cmd.startswith("npm:"): ini.npm(cmd[4:].split())

    @classmethod
    def PATH(cls,path:str):
        if path not in os.environ["PATH"]:
            echo(path,"missing and added to PATH")
            os.environ["PATH"] = f"{path}:{os.environ['PATH']}"
        else:
            verbose(path,"already in PATH and not added")


  #############################################################################
 ########## COMMAND LINE INTERFACE ###########################################
#############################################################################

# initial loading of default backend features
# can be started from cli, py import, or within jupyter notebook
set_backend()

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

    #FIXME: don't use -p within any subcommands
    cli.add("-p",dest="project",action="store",#const=_project_,
        help="set a project name different of sweetheart")

    cli.add("-v","--verbose",action="count",
            help="get additional messages about on-going process")

    cli.add("-c","--conffile",action="store_true",
        help=f"load config from configuration file: {_.conffile}")

    cli.add("-i","--init",action="store_true",
        help="launch init process for building new sweetheart project")

    cli.add("--edit-config",action="store_true",
        help="provide a default configuration json file")

    #FIXME: provisional dev tool:
    cli.add("--update-cloud",action="store_true")


    # create the subparser for the "shell" command:
    cli.sub("shell",help="execute a script given by the current config")
    cli.set(shell)

    cli.add("script",nargs='+',
        help=f'{ "|".join(_config_["scripts"].keys()) }')


    # creat the subparser for the 'book' command:
    cli.sub("book",help="provide full featured documentation from markdown files")
    cli.set(mdbook.commandLine)

    cli.add("name",nargs="?",default="",
        help="name of the documentation root directory")

    cli.add("-a","--anywhere",action="store_true",
        help=f"set the current dir as a documentation dir")

    cli.add("-i","--init",action="store_true",dest="newbook",
        help="create a new empty documentation root directory")

    cli.add("-b","--build",action="store_true",
        help="init/build html documentation from markdown files")

    cli.add("-o","--open",action="store_true",
        help="open html documentation within webbrowser")


    # create the subparser for the "start" command:
    cli.sub("start",help="start required services for running webapps")
    cli.set(lambda args: quickstart())

    cli.add("-x","--mongo-disabled",action="store_true",
        help="start without the mongo database server")

    cli.add("-a","--webapp",action="store_true",
        help="start within the webbrowser as an app")

    cli.add("-j","--jupyter",action="store_true",
        help="start the enhanced jupyterlab server")

    cli.add("-c","--cherrypy",action="store_true",
        help="start cherrypy as an extra webserver for static contents")

    cli.add("-m","--multi-thread",action="store_true",
        help="start uvicorn webserver allowing multi-threading")


    # create the subparser for the "install" command:
    cli.sub("install",help="install given extra packages using apt,cargo,pip,npm")
    cli.set(ini.install)

    cli.add("packages",nargs='+',
        help=f'{ "|".join(_config_["pkg-install"].keys()) }')


    # create the subparser for the "run-jupyter" command:
    cli.sub("run-jupyter",help="run JupyterLab notebook server")
    cli.set(jupyter.commandLine)

    cli.add("-P","--password",action="store_true",
        help="ask for setting server password (can be empty)")
    
    cli.add("-n","--notebook",action="store_true",
        help="open jupyter notebook within webbrowser")

    cli.add("-l","--lab",action="store_true",
        help="start the JupyterLab application within webbrowser")

    cli.add("-H","--home",action="store_true",
        help=f"set {os.environ['HOME']} directory as the working dir")

    cli.add("-k","--set-kernel",action="store_true",
         help="init ipykernel setting within sweetheart python env")


    # create the subparser for the "run-mongod" command:
    cli.sub("run-mongod",help="run MongoDB server daemon")
    cli.set(_mongo_.commandLine)

    # create the subparser for the "run-cherrypy" command:
    cli.sub("run-cherrypy",help="run CherryPy webserver for serving statics")
    cli.set(lambda args: CherryPy.commandLine(args))


    argv = cli.parse()

    # update _config_ from json conf file when required:
    if argv.conffile: ConfigAccess.update()
    
    # update current settings when required:
    ConfigAccess.verbose = getattr(argv,"verbose",_.verbose)
    ConfigAccess.webapp = getattr(argv,"webapp",_.webapp)
    ConfigAccess.jupyter = getattr(argv,"jupyter",_.jupyter)

    mongo_disabled = getattr(argv, "mongo_disabled", mongo_disabled)
    cherrypy_enabled = getattr(argv, "cherrypy", cherrypy_enabled)
    multi_threading = getattr(argv, "multi_thread", multi_threading)

    if argv.project is not None:
        #FIXME: possible unexpected behaviors
        echo("custom project name given:",argv.project)
        _project_ = argv.project
    
    # start early processes when required:
    if argv.update_cloud: cloud.update_files()
    if argv.edit_config: ConfigAccess.edit()
    if argv.init: ini(argv)


  #############################################################################
 ########## CHERRYPY FACILITIES ##############################################
#############################################################################

try:
    import cherrypy
    ConfigAccess.cherrypy = True

    class CherryPy(SwServer):
        """provide cherrypy server facilities

        cherrypy can be used optionnaly for serving static contents
        such server is very stable and keeps performances at high level
        """

        def __init__(self,*args,**kwargs):
            super(CherryPy,self).__init__(*args,**kwargs)

        def cmd(self) -> str:
            #FIXME: to test
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


  #############################################################################
 ##########  WEBAPP FACILITIES ###############################################
#############################################################################

from starlette.applications import Starlette
from starlette.responses import HTMLResponse,FileResponse,RedirectResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

for module in _config_["py-imports"].keys():

    objectToImport = _config_["py-imports"].get(module)
    if _.verbose==2: print(f"** from {module} import {objectToImport}")
    # import selected objects from module:
    if objectToImport: exec(f"from {module} import {objectToImport}")
    # or import module:
    else: exec(f"import {module}")
    del objectToImport, module


# convenient function for rendering html content
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
            <p>{_config_["description"]}</p>
            <p><a href="documentation/index.html"
                class="btn" role="button">Get Started Now!</a></p>
            <p><br>or code immediately using <a href="jupyter">JupyterLab</a></p>
            <p><br><br><em>this message appears because there
                was nothing else to render here</em></p>
            </div>""")

    template_path = os.path.join(_config_["templates_dir"],source)
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
    if not mongo_disabled:
        _mongo_.run_local(service=True)
        _mongo_.set_client(select=_config_["db_select"])
    else: echo("MongoDB server/client DISABLED")

    # set mdbook service:
    if _.mdbook: 
        mdbook.run_local(_config_["working_dir"],service=True)
    else: verbose("mdBook local server is disabled")

    # set mdbook service:
    if _.jupyter: jupyter.run_local(service=True)
    else: verbose("JupyterLab local server is disabled")

    # set the current working directory:
    os.chdir(_config_["working_dir"])
    echo("set working directory:", os.getcwd())
    
    # then build routing depending of given arguments:
    if isinstance(routes,dict):
        echo("create and route starlette objects from dict")
        for segment,endpoint in routes.items():
            webapp.append( Route(segment,endpoint) )
            verbose("callable segment:",callable(endpoint),"",segment)

    elif isinstance(routes,str) and endpoint is None:
        echo("route directly given html content at /")
        webapp.append( Route("/", lambda request: html(routes)) )

    elif routes is None and endpoint is None:
        echo("route a default welcome message at", async_host)
        webapp.append( Route("/", html("WELCOME")) )

    elif callable(routes) and endpoint is None:
        echo("route a single webpage at", async_host)
        webapp.append( Route("/", routes) )
    else:
        raise ValueError("invalid given arguments")

    if cherrypy_enabled:
        # start cherrypy as external service:
        # this will happen with bash command 'sweet -c start'
        echo("try running cherrypy webserver as service")
        staticserver.run_local(service=True)

    # set routing and create Starlette object:
    webapp.mount(route_options=True)
    
    # auto start the webapp within webbrowser:
    if _.webapp: webbrowser(async_host)

    # at last start the uvicorn webserver:
    ConfigAccess.quickstart = True
    uvicorn.run_local(webapp.star)


class WebApp(UserList):

    # provide a mounting tracker
    is_mounted = False

    # default urls endpoints:
    #NOTE: 'request' argument required for rendering methods

    def jupyter(self, request):
        jupyter.run_local(service=True)
        return RedirectResponse(jupyter_host)

    # webapp settings:
    # methodes for main settings: mount() star

    def mount(self,routes=[],route_options=True):
        """set optionnal routing and mount static dirs"""

        # set given routes
        self.extend(routes)

        # route options if required
        if route_options:
            self.extend([
                Route("/favicon.ico",FileResponse(_["static_files.favicon"])),
                Route("/jupyter",self.jupyter),
                Route("/welcome",html("WELCOME")),
                Route("/login",html("login.txt")),
            ])      
        # mount static resources
        self.extend([ Mount(path,StaticFiles(directory=dir)) \
            for path,dir in _config_["static_dirs"].items() ])

        # set tracker
        self.is_mounted = True
        
    @property
    def star(self) -> Starlette:
        # typical use: uvicorn.run(webapp.star)

        # set a default webapp if not mounted
        if self.is_mounted is False:
            self.mount([
                Route("/",RedirectResponse(f"{async_host}/welcome"))
            ])
        # check webapp settings
        for i, route in enumerate(webapp):
            if _.verbose == 2: verbose(i+1,"  type:", type(route))
            assert isinstance(route,Route) or isinstance(route,Mount)

        return Starlette(debug=True,routes=self)

    # allow serving statics with cherrypy:
    #NOTE: optional for getting better performances

    @cherrypy.expose
    def default(self):
        return """
        <link rel="stylesheet" href="/resources/knacss.css">
        <div class="txtcenter">
        <h1><br><br>I'm Ready<br><br></h1>
        <h3>cherrypy server is running</h3>
        </div>"""

    @cherrypy.expose
    def static(self):
        raise NotImplementedError

# set a default webapp object:
webapp = WebApp()


  #############################################################################
 ########## COMMAND LINE & MESSAGES SETUP ####################################
#############################################################################

if __name__ == "__main__":
    
    if not hasattr(argv,"script")\
        and not hasattr(argv,"name")\
        and not hasattr(argv,"notebook"):

        # inform about current version:
        echo(_config_["description"])
        verbose("sweet.py running version:", __version__)
        verbose("written by ", __author__)
        verbose(f"shared under {__license__}\n")

        if _.verbose and _.winapp:
            # give the current wsl statement:
            verbose("current WSL statement:")
            subprocess.run("cmd.exe /c 'wsl -l -v'",shell=True)
            print("")

        if _.verbose == 2:
            # provide the available public objects list:
            objects = dict( (k,v) for k,v in globals().items() \
                if k[0] != "_" and not repr(v).startswith("<module") )
            print("** available objects provided by sweet.py: **\n")
            import pprint
            pprint.pprint(objects); print()

        # force config and settings:
        if not _.cherrypy: cherrypy_enabled = False

        if _.verbose and _project_ != "sweetheart":
            echo(f"config built for the {_dir_[1:3]} project directory")

        # release stacked messages:
        echo(mode="release")
    
    # execute dedicated function related to the cli:
    argv.func(argv)
