from mvc.models.model import Model
from mvc.models.database import Database
from .processing import Processing

import requests
from bs4 import BeautifulSoup
import numpy as np
import urllib.parse
import zipfile
import io
import pandas as pd

class Controller:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.parser = BeautifulSoup(self.response.text, 'html.parser')
        self.model = Model()
        self.database = Database()
        self.processing = Processing


    def request(self):          
        try:
            links = self.parser.find_all('a')
            # Extrair os arquivos CSV do arquivo ZIP em memória
            for link in links:
                zip_name = link.get('href')

                if zip_name.endswith('.zip'):
                    print(zip_name)
                    url_file = urllib.parse.urljoin(self.url, zip_name)
                    zip_data = requests.get(url_file).content
                    zipfile_obj = zipfile.ZipFile(io.BytesIO(zip_data))
                    csv_files = [file for file in zipfile_obj.namelist()]
                    # Ler os arquivos CSV e converter para formato JSON
                    data = []
                    for csv_file in csv_files:
                        csv_data = zipfile_obj.read(csv_file)
                        df = pd.read_csv(io.StringIO(csv_data.decode('latin1')), 
                                        sep=';', encoding='latin1')
                    
                        self.file_type(zip_name, df)
                        
            print('Todos os dados foram enviados com sucesso.')

        except Exception as e:
            print(f"Erro ao realizar a requisição: {str(e)}")
        

    def file_type(self, name, data):
        try:
            self.name = name.split(".")[0]

            if self.name.startswith('Empresas'):
                data = self.processing.data_empresas(self.name, data)
                self.database.insert(self.name, data)

            elif self.name.startswith('Estabelecimento'):
                data = self.processing.data_estabelecimento(self.name, data)
                self.database.insert(self.name, data)

            elif self.name.startswith('Socios'):
                data = self.processing.data_socios(self.name, data)
                self.database.insert(self.name, data)

            elif self.name.startswith('Lucro') or self.name.startswith('Imunes'):
                data = self.processing.data_lucros(self.name, data)
                self.database.insert(self.name, data)

        except Exception as e:
            print(f"Erro ao processar o arquivo: {str(e)}")


    def export_data(self, collection):
        try:
            porcentagem_ativas, ano_empresas = self.database.query(collection)

            df_porcentagem = pd.DataFrame({"Porcentagem de empresas ativas": 
                                        [porcentagem_ativas]})
            df_porcentagem.to_csv("porcentagem_empresas_ativas.csv", index=False)

            df_quantidade_empresas = pd.DataFrame(ano_empresas.items(), 
                                        columns=["Ano", "Quantidade de empresas"])
            df_quantidade_empresas.to_csv(
                "quantidade_empresas_restaurante_por_ano.csv", index=False)

            with pd.ExcelWriter("resultados.xlsx") as writer:
                df_porcentagem.to_excel(writer, 
                                        sheet_name="Porcentagem Empresas Ativas", 
                                        index=False)
                df_quantidade_empresas.to_excel(writer, 
                            sheet_name="Quantidade Empresas Restaurante por Ano", 
                            index=False)
                
        except Exception as e:
            print(f"Erro ao exportar os dados: {str(e)}")
