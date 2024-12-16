import json
from datasets import Dataset

# Exemplo de lista de dicionários
dados = [
]

with open('dados.json', 'r', encoding='utf-8') as arquivo:
    dadosatuais = json.load(arquivo)  # Carrega o conteúdo do JSON em um dicionário ou lista
    for dado in dadosatuais:
        dados.append(dado)


ds = Dataset.from_list(dados)
ds.to_csv('dataset.csv')
