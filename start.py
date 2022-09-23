
from sweetheart.sweet import set_config
from sweetheart.heart import HttpServer,HTMLTemplate,Route

config = set_config({
    "run": "productive" })

webapp = HttpServer(config).app(
    Route("/login",HTMLTemplate("login.htm")) )
