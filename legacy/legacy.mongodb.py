
# class MongoDB(BaseService):

#     def __init__(self,config:BaseConfig,run_local:bool=False):
#         """ set Mongo Database as a service """

#         # url auto set from config
#         super().__init__(config.database_host,config)
#         self.command = f"mongod --dbpath={config.subproc['mongopath']}"
#         if run_local: self.run_local(service=True)
        
#     def set_client(self):
#         """ set MongoDB client and select database given by config 
#             it provides default messages related to the database 
#             return pymongo.MongoClient, MongoClient.Database tuple """

#         from pymongo import MongoClient

#         self.client = MongoClient(host=self.host,port=self.port)
#         echo("available databases:",self.client.list_database_names()[3:])

#         self.database = self.client[self.config['db_name']]
#         echo(f"selected database:",self.config['db_name'])
#         echo("existing collections:",self.database.list_collection_names())

#         return self.client,self.database

#     def on_receive(self,websocket,data):

#         # collection.find_one(data['select'],{'_id':0})
#         # collection.update_one(data['select'],{'$set':data['values']})
#         # collection.insert_one(data['values'])
#         raise NotImplementedError
