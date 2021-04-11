
from sweetheart.globals import *
from sweetheart.sweet import set_config as _set_config_
from sweetheart.sweet import webbrowser,install,quickstart,sws
from sweetheart.heart import Database,HttpServer,Notebook

from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse,FileResponse,RedirectResponse


def set_config(*args,**kwargs):
    """ altered set_config() function for running within jupyter """

    config = _set_config_(*args,**kwargs)
    config.is_webapp_open = True
    config.is_mongodb_local = False
    return config


def HTMLTemplate(*args,**kwargs):
    """ provide a Starlette-like function for templates"""
    if not hasattr(BaseConfig,"_"): set_config()
    return HttpServer(BaseConfig._).HTMLTemplate(*args,**kwargs)
    