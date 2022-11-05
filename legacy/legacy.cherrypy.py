

# try: import cherrypy
# except:
#     class cherrypy:
#         @staticmethod
#         def expose(*args):
#             """ set cherrypy.expose as a ghost method """
#             pass


# class HttpStaticServer(BaseService):

#     def __init__(self,config:BaseConfig,run_local:bool=False):
#         """ set cherrypy as a service for serving static contents
#             should be used for improving server performances if needed """

#         # auto set url from config
#         super().__init__(config.static_host,config)
#         self.command =\
#             f"{config.python_bin} -m sweetheart.sweet cherrypy-server"
#         if run_local: self.run_local(service=True)

#     @cherrypy.expose
#     def default(self):
#         return """
#           <div style="text-align:center;">
#             <h1><br><br>I'm Ready<br><br></h1>
#             <h3>cherrypy server is running</h3>
#           </div>"""

#     def run_local(self,service):
#         """ run CherryPy for serving statics """
#         if service: sp.terminal(self.command,self.terminal)
#         else: cherrypy.quickstart(self,config=self.config.subproc['cherryconf'])
