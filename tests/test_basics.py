
from sweetheart import *

def test_init():
    from sweetheart.install import init
    init( config= set_config(project="test") )
    sp.shell("rm -r ~/.sweet/test")

def test_jupyterlab():
    from sweetheart.services import JupyterLab
    config = set_config(project='jupyter')
    JupyterLab(config).run_local(service=None)

def test_httpserver():
    from sweetheart.services import HttpServer
    config = set_config(project='jupyter')
    HttpServer(config).run_local(service=None)
