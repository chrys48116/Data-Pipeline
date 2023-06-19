from mvc.models.model import Model
from mvc.models.database import Database

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


    def request(self):          
        #zip_data = response.content
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
                    df = pd.read_csv(io.StringIO(csv_data.decode('latin1')), sep=';', encoding='latin1')
                
                    self.file_type(zip_name, df)
                    
        print('Todos os dados foram enviados com sucesso.')


    def file_type(self, name, data):
        self.name = name.split(".")[0]

        if self.name.startswith('Empresas'):
            self.processing_empresas(self.name, data)
            self.database.insert(self.name, data)

        elif self.name.startswith('Estabelecimento'):
            data = self.processing_estabelecimento(self.name, data)
            self.database.insert(self.name, data)

        elif self.name.startswith('Socios'):
            self.processing_socios(self.name, data)
            self.database.insert(self.name, data)


    def processing_empresas(self, name, data):
        pass


    def processing_socios(self, name, data):
        self.name = name.split(".")[0]

        print(data)
        print(f'Processando dados: {self.name}.')
        data['CNPJ'] = data[data.columns[0]]
        dados = self.model.archives_parser('socios')
        data['ID Socio'] = data[data.columns[1]].map(dados)
        data['Nome Socio'] = data[data.columns[2]]

        dados = self.model.archives_parser('qualificacao')
        data['Qualificação'] = data[data.columns[4]].map(dados)

        data['Data Entrada Sociedade'] = data[data.columns[5]].astype(str)
        data['Data Entrada Sociedade'] = data['Data Entrada Sociedade'].apply(lambda x: f"{x[6:]}/{x[4:6]}/{x[:4]}")

        dados = self.model.archives_parser('paises')
        data['CO-Pais'] = data[data.columns[6]].map(dados)

        dados = self.model.archives_parser('qualificacao')
        data['Qualificação Representante'] = data[data.columns[9]].map(dados)

        data['Registro'] = data[data.columns[10]]

        data_final = data[['CNPJ','ID Socio','Qualificação','Data Entrada Sociedade','CO-Pais','Qualificação Representante','Registro']]
        data_final = data_final.to_dict(orient='records')

        return data_final


    def processing_estabelecimento(self, name, data):
        self.name = name.split(".")[0]
        print(data)
        print(f'Processando dados: {self.name}.')

        data['CNPJ'] = data[data.columns[0]].astype(str)
        data['CNPJ'] = data[data.columns[1]].astype(str)
        data['CNPJ'] = data[data.columns[2]].astype(str)
        data['CNPJ'] = data.iloc[:, :3].astype(str).apply(lambda row: '.'.join([str(val) for val in row]), axis=1) #TODO: arrumar 0001
        data['CNPJ'] = data['CNPJ'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        data['Matriz/Filial'] = np.where(data[data.columns[3]]==1, 'Matriz', 'Filial')
        data['Matriz/Filial'] = data['Matriz/Filial'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        data['Razão Social/Nome'] = data[data.columns[4]]
        data['Razão Social/Nome'] = data['Razão Social/Nome'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        dados = self.model.archives_parser('situacao')
        data['Situação Cadastral'] = data[data.columns[5]].map(dados)
        data['Situação Cadastral'] = data['Situação Cadastral'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        data['Data Situação Cadastral'] = data[data.columns[6]].astype(str)
        data['Data Situação Cadastral'] = data['Data Situação Cadastral'].apply(lambda x: f"{x[6:]}/{x[4:6]}/{x[:4]}")
        data['Data Situação Cadastral'] = data['Data Situação Cadastral'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))
        
        dados = self.model.archives_parser('motivos')
        data['Motivo Situação Cadastral'] = data[data.columns[7]].map(dados)
        data['Motivo Situação Cadastral'] = data['Motivo Situação Cadastral'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))
        
        dados = self.model.archives_parser('paises')
        data['CO-Pais'] = data[data.columns[9]].map(dados)
        data['CO-Pais'] = data['CO-Pais'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        data['Data Inicio Atividade'] = data[data.columns[10]].astype(str)
        data['Data Inicio Atividade'] = data['Data Inicio Atividade'].apply(lambda x: f"{x[6:]}/{x[4:6]}/{x[:4]}")
        data['Data Inicio Atividade'] = data['Data Inicio Atividade'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        dados = self.model.archives_parser('cnae')
        data['Cnae-Fiscal'] = data[data.columns[11]].map(dados)
        data['Cnae-Fiscal'] = data['Cnae-Fiscal'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))
        data['Cnae-Fiscal2'] = data[data.columns[12]].map(dados)
        data['Cnae-Fiscal2'] = data['Cnae-Fiscal2'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        data['Numero'] = data[data.columns[15]].apply(lambda x: x if x != '' else 'S/N')

        data['Complemento'] = data[data.columns[13]]
        data['Complemento'] = data['Complemento'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        data['Bairro'] = data[data.columns[14]]
        data['Bairro'] = data['Bairro'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        data['CEP'] = data[data.columns[18]]
        data['CEP'] = data['CEP'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        data['UF'] = data[data.columns[19]]
        data['UF'] = data['UF'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))
        
        dados = self.model.archives_parser('municipio')
        data['Codigo Municipio'] = data[data.columns[20]].map(dados)   
        data['Codigo Municipio'] = data['Codigo Municipio'].fillna(pd.NaT).astype(str).apply(lambda x: x.replace('.nan', ''))

        #data['DDD-Telefone'] =pd.to_numeric(data[data.columns[21]]) + pd.to_numeric(data[data.columns[22]])
        data['DDD-Telefone'] = data.apply(lambda row: str(row[data.columns[21]]) + str(row[data.columns[22]]), axis=1).apply(lambda x: x if x != '' else 'null')
        data['DDD-Telefone2'] = data.apply(lambda row: str(row[data.columns[23]]) + str(row[data.columns[24]]), axis=1).apply(lambda x: x if x != '' else 'null')
        data['DDD-Fax'] = data.apply(lambda row: str(row[data.columns[25]]) + str(row[data.columns[26]]), axis=1).apply(lambda x: x if x != '' else 'null')

        data['E-mail'] = data[data.columns[27]]

        data_final = data[['CNPJ','Matriz/Filial','Razão Social/Nome','Situação Cadastral','Data Situação Cadastral','Motivo Situação Cadastral','CO-Pais','Data Inicio Atividade','Cnae-Fiscal','Cnae-Fiscal2','Numero','Complemento','Bairro','CEP','UF','Codigo Municipio','DDD-Telefone','DDD-Telefone2','DDD-Fax','E-mail']]
        data_final = data_final.to_dict(orient='records')

        return data_final


url = "https://dadosabertos.rfb.gov.br/CNPJ/"
controller = Controller(url)
controller.request