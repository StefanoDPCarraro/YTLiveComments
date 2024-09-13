import json
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
from collections import Counter

def get_author_comments(author, comments_json, interval=30):
    with open(comments_json, 'r') as file:
        data = json.load(file)

    author_comments = []
    for item in data:
        if item['author'] == author:
            author_comments.append(item)
    
    author_filtered_comments = [comment for comment in author_comments if comment['message'].strip()]

    df = pd.DataFrame(author_filtered_comments)
    df['timestamp'] = pd.to_datetime(df['time_elapsed'])
    df.set_index('timestamp', inplace=True)
    resampled_df = df.resample(f'{interval}T').size()

    plt.figure(figsize=(14, 6))
    plt.plot(resampled_df.index, resampled_df.values)
    plt.xlabel('Tempo')
    plt.ylabel('Comentários')
    plt.title(f'Comentários a cada {interval} minutos')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.grid(True)

    path = f'output/comentarios_{author}_por_minuto.png'

    plt.savefig(path)

    return path, author_filtered_comments

def get_top_authors(comments_json, n=5):
    with open(comments_json, 'r') as file:
        data = json.load(file)

    filter_data = [item for item in data if item['message'].strip()]

    authors = [item['author'] for item in filter_data]
    author_freq = Counter(authors)

    top_authors = author_freq.most_common(n)
    return top_authors

