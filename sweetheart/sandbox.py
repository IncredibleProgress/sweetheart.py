"""
sandbox.py is dedicated for making tests and fast prototyping 
it allows getting usual objects you would need importing only one module
"""

print("[SANDBOX] this module is given for tests not for production")

# patch running within JupyterLab
import nest_asyncio
nest_asyncio.apply()

from sweetheart import *
from sweetheart.install import BaseInstall
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
