import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

def file_to_json(json_file):    
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

# Baixar stopwords em português, se ainda não estiver disponível
nltk.download('stopwords')

# Função para processar o JSON e gerar a nuvem de palavras
def gerar_nuvem_palavras(json_data, complemento=''):
    # Carregar o arquivo JSON
    

    # Inicializar uma lista para armazenar todas as palavras
    all_words = []

    # Processar cada item no JSON
    for item in json_data:
        # Converter a mensagem para minúsculas
        message = item['message'].lower()
        # Separar a mensagem em palavras e adicionar à lista
        words = message.split()
        all_words.extend(words)

    # Criar uma string com todas as palavras
    text = ' '.join(all_words)

    # Baixar stopwords em português
    stop_words = set(stopwords.words('portuguese'))

    # Criar a nuvem de palavras
    wordcloud = WordCloud(stopwords=stop_words, background_color='white', width=1920, height=1080).generate(text)

    # Criar a pasta 'output' se não existir
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Caminho para salvar o arquivo
    output_file = os.path.join(output_dir, f'nuvem_palavras{complemento}.png')

    # Salvar a nuvem de palavras em um arquivo
    wordcloud.to_file(output_file)
    print(f'Nuvem de palavras salva em: {output_file}')

    return output_file