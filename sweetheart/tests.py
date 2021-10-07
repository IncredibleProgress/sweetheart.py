
from sweetheart.globals import *
from sweetheart.sweet import *
from sweetheart.heart import *


def test_version():
    from sweetheart import __version__
    assert __version__ == '0.1.1'

def test_init():
    from sweetheart.sweet import set_config
    from sweetheart.install import init
    assert init(config=set_config(project="test"))
    sp.shell("rm -r ~/.sweet/test")

def test_template(template:str):
    
    BaseConfig.verbosity = 1
    config =  set_config(sandbox=False)
    webapp = HttpServer(config)

    database = RethinkDB(config)
    websocket = database.set_websocket()
    redb,conn = database.set_client()

    webapp.mount(
        Route("/test",webapp.HTMLTemplate(template)),
        WebSocketRoute("/database",websocket) )

    webapp.run_local(service=False)


if __name__ == '__main__':

    # starting tests from sws
    from sys import argv
    test_version()
    test_template(argv[-1])
