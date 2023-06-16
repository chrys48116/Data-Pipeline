import pandas as pd
from pymongo import MongoClient

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
