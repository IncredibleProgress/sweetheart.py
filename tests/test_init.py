
from sweetheart.globals import *
from sweetheart.sweet import set_config
from sweetheart.install import init

def test_init():
    init(config=set_config(project="test"))
    sp.shell("rm -r ~/.sweet/test")
