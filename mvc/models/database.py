from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://chrystian:chrystianartur16@cluster0.9bva9n6.mongodb.net/")
        self.db = self.client['Cluster0']

    def insert(self, zip_name, data):
        collection = self.db[f'{zip_name.split(".")[0]}']
        # Inserir os documentos na coleção
        collection.insert_many(data)
        print("Dados inseridos no MongoDB Atlas com sucesso.")

