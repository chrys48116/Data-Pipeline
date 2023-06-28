from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        """Inicializa a conexão com o MongoDB Atlas.

        A função cria uma conexão com o MongoDB Atlas utilizando as credenciais fornecidas.
        A conexão estabelecida permite acessar o banco de dados e realizar operações nele.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.

        """
        load_dotenv()
        user= os.environ['USER'],
        try:
            self.client = MongoClient(user)
            self.db = self.client['Cluster0']
            print("Conexão com o MongoDB Atlas estabelecida com sucesso.")
        except Exception as e:
            print(f"Erro ao conectar com o MongoDB Atlas: {str(e)}")


    def insert(self, zip_name, data):
        """Insere os dados em uma coleção do MongoDB Atlas.

        Esta função recebe o nome do arquivo ZIP e os dados a serem inseridos.
        Utiliza o nome do arquivo para determinar o nome da coleção no MongoDB Atlas.
        Os dados são inseridos na coleção especificada.

        Args:
            zip_name (str): O nome do arquivo ZIP.
            data (list): Os dados a serem inseridos na coleção.

        Returns:
            None.

        Raises:
            None.

        """
        try:
            collection = self.db[f'{zip_name.split(".")[0]}']
            collection.insert_many(data)
            print("Dados inseridos no MongoDB Atlas com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir dados no MongoDB Atlas: {str(e)}")


    def query(self, table_name):
        """Realiza uma consulta na coleção especificada do MongoDB Atlas.

        Esta função recebe o nome da coleção no MongoDB Atlas e realiza uma 
        série de consultas para obter informações sobre as empresas.

        Args:
            table_name (str): O nome da coleção no MongoDB Atlas.

        Returns:
            tuple: Uma tupla contendo a porcentagem de empresas ativas e um 
            icionário com a quantidade de empresas de restaurantes abertas por ano.

        Raises:
            None.

        """
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
                    "Cnae": {"$regex": f"^{prefixo_restaurante}"},
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