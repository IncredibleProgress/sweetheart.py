
from sweetheart.globals import *


def test_version():
    from sweetheart import __version__
    assert __version__ == '0.1.1'

def test_init():
    from sweetheart.sweet import set_config
    from sweetheart.install import init
    assert init(config=set_config(project="test"))
    sp.shell("rm -r ~/.sweet/test")
