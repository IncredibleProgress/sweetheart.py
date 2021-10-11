
from sweetheart.globals import *
from sweetheart.sweet import *
from sweetheart.heart import *
from sweetheart.install import *


def test_version():
    from sweetheart import __version__
    assert __version__ == '0.1.1'

def test_init():
    assert init(config=set_config(project="test"))
    sp.shell("rm -r ~/.sweet/test")

def test_template(template:str):
    
    BaseConfig.verbosity = 1
    config = set_config(sandbox=False)
    #config.is_webapp_open = True

    webapp = HttpServer(config,set_database=True)
    websocket = webapp.db.set_websocket()
    redb,conn = webapp.db.set_client()

    quickstart( webapp.mount(
        Route("/",HTMLTemplate(template)),
        WebSocketRoute("/database",websocket) ))


if __name__ == '__main__':

    # starting tests from sws
    from sys import argv
    test_version()
    test_template(argv[-1])
