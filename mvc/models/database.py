from pymongo import MongoClient
from datetime import datetime
import pandas as pd

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(
            "mongodb+srv://chrystian:chrystianartur16@cluster0.9bva9n6.mongodb.net/")
            self.db = self.client['Cluster0']
            print("Conexão com o MongoDB Atlas estabelecida com sucesso.")
        except Exception as e:
            print(f"Erro ao conectar com o MongoDB Atlas: {str(e)}")


    def insert(self, zip_name, data):
        try:
            collection = self.db[f'{zip_name.split(".")[0]}']
            collection.insert_many(data)
            print("Dados inseridos no MongoDB Atlas com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir dados no MongoDB Atlas: {str(e)}")


    def query(self, table_name):
        try:
            collection = self.db[table_name]
            total_empresas = collection.count_documents({})
            empresas_ativas = collection.count_documents({"Situação Cadastral": "Ativa"})
            porcentagem_ativas = (empresas_ativas / total_empresas) * 100
            print(f"Porcentagem de empresas ativas: {porcentagem_ativas:.2f}%")

            prefixo_restaurante = "561"
            ano_empresas = {}
            empresas_restaurante = collection.find(
                {
                    "CNAE": {"$regex": f"^{prefixo_restaurante}"},
                    "Data Inicio Atividade": {"$exists": True},
                },
                {"Data Inicio Atividade": 1},
            )

            for empresa in empresas_restaurante:
                data_inicio = empresa["Data Inicio Atividade"]
                ano = datetime.strptime(data_inicio, "%Y-%m-%d").year
                if ano in ano_empresas:
                    ano_empresas[ano] += 1
                else:
                    ano_empresas[ano] = 1
                
            print("Quantidade de empresas de restaurantes abertas por ano:")
            for ano, quantidade in ano_empresas.items():
                print(f"Ano {ano}: {quantidade} empresas")

            return porcentagem_ativas, ano_empresas
    
        except Exception as e:
                print(f"Erro ao consultar dados no MongoDB Atlas: {str(e)}")
                return None, None