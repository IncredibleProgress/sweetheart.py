
from sweetheart.globals import *
from sweetheart.sweet import *
from sweetheart.heart import *
from sweetheart.install import *

from sweetheart import __version__
assert __version__ == '0.1.1'

def test_init():
    init(config=set_config(project="test"))
    sp.shell("rm -r ~/.sweet/test")

def test_template(template:str):
    
    BaseConfig.verbosity = 1
    config = set_config(sandbox=False)
    #config.is_webapp_open = True

    webapp = HttpServer(config,set_database=True)
    quickstart( webapp.mount(
        Route("/",HTMLTemplate(template)) ))

if __name__ == '__main__':

    # make tests from sws
    from sys import argv
    if '--init' in argv: test_init()
    else: test_template(argv[-1])
