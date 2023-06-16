import pandas as pd
from pymongo import MongoClient
def teste():
    # Passo 1: Leitura dos dados

    # Ler os arquivos CSV usando o pandas
    estabelecimento_df = pd.read_csv('caminho/para/arquivo/estabelecimento.csv', sep=';', encoding='latin1')

    # Passo 2: Organização dos dados

    # Converter o dataframe para um dicionário
    estabelecimento_data = estabelecimento_df.to_dict(orient='records')

    # Passo 3: Banco de dados

    # Configurar a conexão com o banco de dados MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['nome_do_banco_de_dados']
    collection = db['nome_da_colecao']

    # Passo 4: Salvando os dados no banco de dados

    # Inserir os dados na coleção
    collection.insert_many(estabelecimento_data)

    # Passo 5: Leitura e processamento dos dados

    # Recuperar os dados do banco de dados
    estabelecimento_data = collection.find()

    # a) Calcular a porcentagem de empresas ativas (SITUAÇÃO CADASTRAL)
    total_empresas = estabelecimento_data.count()
    empresas_ativas = collection.count_documents({"SITUAÇÃO CADASTRAL": "02 - Ativa"})
    porcentagem_ativas = (empresas_ativas / total_empresas) * 100

    # b) Filtrar as empresas do setor de restaurantes
    restaurantes_data = collection.find({
        "CNAE FISCAL PRINCIPAL": {"$regex": "^56.1"},
        "DATA DE INÍCIO ATIVIDADE": {"$exists": True}
    })

    # c) Contar a quantidade de empresas de restaurantes abertas em cada ano
    restaurantes_por_ano = restaurantes_data.groupby(estabelecimento_df['DATA DE INÍCIO ATIVIDADE'].dt.year).size()

    # Exemplo de exibição dos resultados
    print(f"Porcentagem de empresas ativas: {porcentagem_ativas:.2f}%")
    print(restaurantes_por_ano)

import requests
import zipfile
import io
import pandas as pd
from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.parse
def teste2():

    # URL do arquivo ZIP
    url = "https://dadosabertos.rfb.gov.br/CNPJ/"

    # Fazer a requisição HTTP para obter o conteúdo do arquivo ZIP
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    zip_data = response.content
    links = soup.find_all('a')
    # Extrair os arquivos CSV do arquivo ZIP em memória
    for link in links:
        href = link.get('href')
        print(href)
        if href.endswith('.zip'):
            url_arquivo = urllib.parse.urljoin(url, href)
            zip_data = requests.get(url_arquivo).content
            #print(zip_data)

            zipfile_obj = zipfile.ZipFile(io.BytesIO(zip_data))
            csv_files = [file for file in zipfile_obj.namelist()]
            print(csv_files)

            # Ler os arquivos CSV e converter para formato JSON
            json_data = []
            for csv_file in csv_files:
                csv_data = zipfile_obj.read(csv_file)
                df = pd.read_csv(io.StringIO(csv_data.decode('latin1')), sep=';', encoding='latin1')
                hash = json_data.extend(df.to_dict(orient='records'))
                print(hash)

                # Configurar a conexão com o MongoDB Atlas
                client = MongoClient("mongodb+srv://chrystian:chrystianartur16@cluster0.9bva9n6.mongodb.net/")

                # Selecionar o banco de dados e a coleção
                db = client['Cluster0']
                collection = db['nome_da_colecao']

                # Inserir os documentos na coleção
                collection.insert_many(json_data)

                print("Dados inseridos no MongoDB Atlas com sucesso.")
teste2()