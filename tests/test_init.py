
from sweetheart import *

def test_init():
    from sweetheart.install import init
    init(config=set_config(project="test"))
    sp.shell("rm -r ~/.sweet/test")
