""" sweetheart.py

full power for newbies built on highest quality components

- easy to learn, easy to use
- quick and clean prototyping
- quick and clean deployement
- ready for maintenable great code quality
- ready for datacenters, big-data and ai
- ready for inovation and creativity

sweetheart is python/html/css centric meaning that you will
find support and skilled people for low costs everywhere
(e.g. through projects with studients)

a supercharged heart like used by gafam in your non-expert hands
go farer ahead now !
"""

__version__ = "0.0.1dev"
__license__ = "CeCILL-C"

import cherrypy #> powerfull web server and facilities
import os, sys #> usual python tools for general purposes
import argparse #> official python command-line parsing module
import mistune #> a better markdown parser for getting html
from pymongo import MongoClient #> official connector for MongoDB databases
from bottle import template #> for use of the SimpleTemplateEngine


# provide default configuration:

_config_ = {
    "database": {
        "host": "localhost",
        "port": 27017,
        "dbpath": "/opt/incredible/database",
        "select": "demo"
    },
    "cherrypy": { # url segments configs:
        "/": "/opt/incredible/configuration/server.conf"
    },
    "display": "DISPLAY=:0",
    "echolabel": "[SWEETHEART]",
    "working_dir": "/opt/incredible/webpages",
    "webbrowser": 'cmd.exe /c start brave.exe --app="http://localhost:8080/"'
}


# re-implement some usual cherrypy objects:
expose = cherrypy.expose
session = lambda: cherrypy.session
cookie = cherrypy.response.cookie
serve_file = cherrypy.lib.static.serve_file
json = lambda: cherrypy.request.json
json_in = cherrypy.tools.json_in
json_out = cherrypy.tools.json_out
HTTPError = cherrypy.HTTPError


# convenient function for printing messages:
def echo(*args):
    print(_config_.get("echolabel",""), *args)


# provide the command line interface (CLI):
_parser_ = argparse.ArgumentParser()

if __name__ == "__main__":

    # exclusive cli positionnal arguments:
    _parser_.add_argument("action", 
        choices = ("start","init"),
        help = "create and configure a new sweetheart poject")
    
    mongo_disabled = "DISABLED"

# shared cli optionnal arguments:
_parser_.add_argument("-v", "--verbosity", action="store_true",
    help = "get some additional messages about processing")
_parser_.add_argument("-x", "--mongo-disabled", action="store_true",
    help = "run without the mongo database server")
_parser_.add_argument("-a", "--webapp", action="store_true",
    help = "start within webbrowser as an app")

argv = _parser_.parse_args()
if argv.mongo_disabled: mongo_disabled = "DISABLED"
echo("start with given args:", sys.argv)


# set current working directory:
os.chdir(_config_["working_dir"])
echo("set working directory:", os.getcwd())


# abstract mongoDB settings:
if "mongo_disabled" not in globals():

    echo("try for getting mongodb client...")
    os.system('%s xterm -C -geometry 190x19 -e \
        mongod --dbpath="%s" &'
        % (_config_['display'],
            _config_['database']['dbpath']))
    
    mongoclient = MongoClient(
        host= _config_['database']['host'],
        port= _config_['database']['port'] )
    
    echo("available databases given by mongoclient:",
        mongoclient.list_database_names() )

    database = mongoclient[ _config_['database']['select'] ]

    echo("connected to the default database:",
        _config_['database']['select'] )

    echo("existing mongodb collections:",
        database.list_collection_names() )

else:
    echo("WARNING: MongoDB client disabled")


# abstract setting multi apps config:
def setconfig(config: dict):
    _config_["cherrypy"].update(config)
    echo("set config routing:", _config_["cherrypy"])


# abstract mounting multi-class:
def mount(routing, url="/", config=_config_["cherrypy"]["/"]):

    if isinstance(routing, dict):
        for segment, object_ in routing.items():

            cherrypy.tree.mount(
                object_,
                segment, 
                _config_["cherrypy"].get(segment, None) )
    
    else: cherrypy.tree.mount(routing, url, config)


# abstract mounting rest dispatching:
def dispatch(dispatch_routing: dict):

    for segment, methods in dispatch_routing.items():

        cherrypy.tree.mount(
            HttpDispatcher(methods),
            segment,
            _config_["cherrypy"].get(segment, {
                "/": { "request.dispatch": 
                    cherrypy.dispatch.MethodDispatcher() } }) )


# starts the web application listening for requests:
def start(route=None, url="/", config=_config_["cherrypy"]["/"]):

    if not route:
        #cherrypy.config.update({'server.socket_host': '0.0.0.0', })
        #cherrypy.config.update({'server.socket_port': port, })
        cherrypy.engine.start()
        cherrypy.engine.block()

    else: cherrypy.quickstart(route, url, config)


# stop the web application
def stop():
    cherrypy.engine.stop()


# convenient function for rendering html content:
def html(source: str = "", **kwargs):
    if not source:
        # provide a welcome message:
        return """
        <link rel="stylesheet" href="knacss.css">
        <div class="txtcenter">
          <h1><br><br>Welcome %s !<br><br></h1>
          <h3>sweetheart.py</h3>
          <p>a supercharged heart for the non-expert hands</p>
          <p>be aware that you could fall in love with it</p>
          <p><a href="" class="btn" role="button">go farer ahead now !</a></p>
          <p><br><br><br><em>this message appears because there
            were nothing else to render here</em></p>
        </div>
        """ % os.environ["USER"].capitalize()
    else:
        # provide html content from template:
        path = os.path.join("bottle_templates", source)
        return template(path, **kwargs)


# abstract the cherrypy dispatch recipe:
@cherrypy.expose()
class HttpDispatcher():
    """
    set related function for each http methods as follow:

        HttpDispatcher({
            "GET": get_function,
            "POST": post_function,
            "PUT":  put_function,
            "DELETE": delete_function })
    """
    def __init__(self, methods):
        self.methods = methods

    @cherrypy.tools.accept(media="text/plain")
    def GET(self, **kwargs):
        self.methods["GET"](**kwargs)

    def POST(self, **kwargs):
        self.methods["POST"](**kwargs)

    def PUT(self, **kwargs):
        self.methods["PUT"](**kwargs)

    def DELETE(self, **kwargs):
        self.methods["DELETE"](**kwargs)


# provide a default rendering class:
class HtmlRoot():

    @cherrypy.expose()
    def index(self):
        return html()

    @cherrypy.expose
    def readme(self):

        with open("markdown_docs/references.md") as file:
            text = file.read()

        return html("document.txt",
            text=mistune.markdown(text),
            header=True)


if __name__ == "__main__":
    """
    Sweetheart provide a convenient command line interface (CLI)
    dedicated to dev/admin tasks and available using the command called 'sweet'
    """
    if argv.action == "start":
        start( HtmlRoot() )
        if argv.webapp: os.system(_config_["webbrowser"])

    elif argv.action == "init": 
        import subprocess

        # set bash commands:
        apt = "sudo apt install".split()
        npm = "/opt/sweetheart/webpages/npm install".split()
        pip = "/opt/sweetheart/programs/envPy/bin/pip install".split()
        wget = "/opt/sweetheart/webpages/usual_resources/wget".split()

        # start install process:
        print("\nsweetheart.py\ninstallation process start now !")
        print("WARNING: root privileges are required to continue")

        print("\nINIT step1: install required packages...")
        subprocess.run( apt + [
            "virtualenv", #> for building isolated python env
            "mongodb", #> database big-data ready
            "xterm", #> lightweight bash terminal

            "npm", #> well known node packages manager
            "node-typescript", # improve javascript code
            "node-vue", #> for building advanced user interfaces
        
            "libjs-vue", #> for building advanced user interfaces
            "libjs-highlight.js", #> powerfull html code highlighting
            "libjs-bootstrap4", #> for building advanced user interfaces
            "libjs-jquery" ]) #> for decreasing javascript coding effort

        print("\nINIT step2: creating directories...")
        os.system("sudo mkdir /opt/sweetheart")
        os.system("sudo mkdir /opt/sweetheart/database")
        os.system("sudo mkdir /opt/sweetheart/programs")
        os.system("sudo mkdir /opt/sweetheart/webpages")
        os.system("sudo mkdir /opt/sweetheart/webpages/usual_resources")
        os.system("ln --symbolic /usr/share/javascript \
            /opt/sweetheart/webpages/javascript_libs")
        os.system("sudo chmod 777 -R /opt/sweetheart")

        print("\nINIT step3: building python env...")
        os.system("virtualenv -p python3 /opt/sweetheart/programs/envPy")
        subprocess.run( pip + [
            "bottle", 
            "pymongo",
            "mistune",
            "openpyxl",
            "cherrypy" ])

        print("\nINIT step4: downloading resources...")
        for url in [
            "https://raw.githubusercontent.com/alsacreations/KNACSS/master/css/knacss.css",
            "https://www.w3schools.com/w3css/4/w3.css" ]:
            subprocess.run( wget + url )

        print("\nINIT step5: downloading node modules...")
        os.system("npm init --yes")
        subprocess.run( npm + [
            "knacss" ])
