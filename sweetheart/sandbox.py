
from sweetheart.globals import *
from sweetheart.sweet import set_config, install
from sweetheart.sweet import webbrowser,install,quickstart,sws
from sweetheart.heart import RethinkDB,HttpServer,JupyterLab,HTMLTemplate as _HTMLTemplate_
from sweetheart.install import BaseInstall

from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse,FileResponse,RedirectResponse

try: import pandas as pa
except: pass


def HTMLTemplate(*args,**kwargs):
    """ provide a Starlette-like function for templates
        altered HTMLTemplate() function for running within jupyter """
    if not hasattr(BaseConfig,"_"): set_config(sandbox=True)
    return _HTMLTemplate_(*args,**kwargs)
    