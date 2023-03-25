"""
sandbox is dedicated for making tests and fast prototyping 
it allows getting usual objects you would need importing only one module
when not given config will be autoset for providing some magic 
"""

#FIXME: patch running within JupyterLab
import nest_asyncio
nest_asyncio.apply()

from sweetheart import *
from sweetheart.cli import sws
from sweetheart.install import BaseInstall
from sweetheart.heart import \
    RethinkDB,\
    HttpServer,\
    JupyterLab,\
    WelcomeMessage,\
    HTMLTemplate as _HTMLTemplate_

from starlette.routing import *
from starlette.staticfiles import *
from starlette.responses import *

try: import pandas as pa
except: pass

# def HTMLTemplate(*args,**kwargs):
#     """ provide a Starlette-like function for templates
#         altered HTMLTemplate() function for running within Jupyter """
#     if not hasattr(BaseConfig,"_"): set_config()
#     return _HTMLTemplate_(*args,**kwargs)
