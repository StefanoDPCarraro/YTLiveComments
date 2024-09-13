import json
from collections import Counter

def get_author_comments(author, comments_json):
    with open(comments_json, 'r') as file:
        data = json.load(file)

    author_comments = []
    for item in data:
        if item['author'] == author:
            author_comments.append(item['message'])
    
    author_filtered_comments = [comment for comment in author_comments if comment.strip()]

    return author_filtered_comments

def get_top_authors(comments_json, n=5):
    with open(comments_json, 'r') as file:
        data = json.load(file)

    filter_data = [item for item in data if item['message'].strip()]

    authors = [item['author'] for item in filter_data]
    author_freq = Counter(authors)

    top_authors = author_freq.most_common(n)
    return top_authors

