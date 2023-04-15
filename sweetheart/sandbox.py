"""
sandbox.py is dedicated for making tests and fast prototyping 
it allows getting usual objects you would need importing only one module
"""

print("[SANDBOX] this module is given for tests not for production")

from sweetheart import *
from sweetheart.install import BaseInstall

del set_config
from sweetheart import set_config as __set_config

from sweetheart.services import \
    RethinkDB,\
    HttpServer,\
    JupyterLab,\
    NginxUnit

from starlette.routing import *
from starlette.staticfiles import *
from starlette.responses import *

try: import pandas as pa
except: pass

# patch running within JupyterLab
import nest_asyncio
nest_asyncio.apply()
__exit = sys.exit

# production settings not available
def set_config(*args,**kwargs) -> BaseConfig:
    config = __set_config(*args,**kwargs)

    if config.run == "productive":
        print("[STOPPED] productive setting forbidden with sandbox")
        __exit()

    return config
