"""
sandbox is dedicated for making tests and fast prototyping 
it allows getting usual objects you would need importing only one module
when not given config will be autoset for providing some magic 
"""

# #FIXME: patch running within JupyterLab
# import nest_asyncio
# nest_asyncio.apply()

from sweetheart import *
#from sweetheart.cli import sws
from sweetheart.install import BaseInstall
from sweetheart.services import \
    RethinkDB,\
    HttpServer,\
    JupyterLab

from starlette.routing import *
from starlette.staticfiles import *
from starlette.responses import *

try: import pandas as pa
except: pass
