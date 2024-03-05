
from pymongo import MongoClient
from config import configuracion

class MongoDBConexion:
    
    def __init__(self): # Constructor que se inicializa automaticamente
        self.client = MongoClient(configuracion.MONGODB_URI)
        self.db = self.client[configuracion.MONGODB_DATABASE]
        
    def busqueda(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find(query)
    
    def insert(self, collection_name, data):
        collection = self.db[collection_name]
        return collection.insert_many(data)
