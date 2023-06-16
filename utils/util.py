import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from tqdm import tqdm
import zipfile
import io
import pandas as pd
from pymongo import MongoClient


def download_files():
    url_base = "https://dadosabertos.rfb.gov.br/CNPJ/"
    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url_base)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a") # Encontra todos os links na página
    pasta_destino = "pipeline\\data" # Pasta de destino para salvar os arquivos baixados
    # Percorre os links e faz o download dos arquivos
    for link in links:
        href = link.get("href")
        print(href)
        if href.endswith(".zip"):
            url_arquivo = urllib.parse.urljoin(url_base, href) # Monta a URL completa do arquivo
            # Extrai o nome do arquivo da URL
            nome_arquivo = href.split("/")[-1]
            # Caminho completo do arquivo de destino
            caminho_arquivo = f"{pasta_destino}/{nome_arquivo}"
            
            arquivos = list()
            for arquivo in os.listdir(pasta_destino):
                arquivos.append(arquivo)
                
            if nome_arquivo in arquivos:
                print(f"Arquivo {nome_arquivo} já existe na pasta.")
            else:
                response = requests.get(url_arquivo, stream=True)
                total_size = int(response.headers.get('content-length', 0))

                with open(caminho_arquivo, "wb") as file, tqdm(
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as progress_bar:
                    for data in response.iter_content(chunk_size=1024):
                        file.write(data)
                        progress_bar.update(len(data))
                print(f"Arquivo {nome_arquivo} baixado com sucesso.")

    print("Arquivos baixados com sucesso!")

download_files()

def extract_read_files(arquivos):
    pasta_destino = "pipeline\\data"
    arquivos = []
    for arquivo in os.listdir(pasta_destino):
        arquivos.append(arquivo)
    for arquivo in arquivos:
        caminho_arquivo = f"{pasta_destino}/{arquivo}"
        if arquivo.endswith(".zip"):
            zip_file = zipfile.ZipFile(caminho_arquivo)
            zip_file.extractall(pasta_destino)
            zip_file.close()
            print(f"Arquivo {arquivo} extraído com sucesso.")

        elif arquivo.split('.')[-1] != ['.csv', '.zip']:
            arquivo = f'{arquivo}.csv'
            os.rename(caminho_arquivo, arquivo)
            print(f"Arquivo {arquivo} renomeado.")
        
        elif arquivo.endswith(".csv"):
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')
            data = df.to_dict(orient='records')
            print(f"Arquivo {arquivo} lido com sucesso.")


def dataBaseConnection():
    client = MongoClient('mongodb://localhost:27017')
    db = client['nome_do_banco_de_dados']
    collection = db['nome_da_colecao']