import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
import re

def file_to_json(json_file):    
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

nltk.download('stopwords')

def gerar_nuvem_palavras(json_data, complemento=''):

    all_words = []

    emoji_pattern = r':[a-zA-Z0-9-]+:'

    for item in json_data:
        message = item['message'].lower()
        message = re.sub(emoji_pattern, '', message)
        words = message.split()
        all_words.extend(words)

    text = ' '.join(all_words)
    stop_words = set(stopwords.words('portuguese'))
    wordcloud = WordCloud(stopwords=stop_words, background_color='white', width=1920, height=1080).generate(text)

    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'nuvem_palavras{complemento}.png')

    wordcloud.to_file(output_file)
    print(f'Nuvem de palavras salva em: {output_file}')

    return output_file