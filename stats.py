import json
from collections import Counter

def get_author_comments(author, comments_json):
    with open(comments_json, 'r') as file:
        data = json.load(file)

    author_comments = []
    for item in data:
        if item['author'] == author:
            author_comments.append(item['message'])

    return author_comments

def get_top_authors(comments_json, n=5):
    with open(comments_json, 'r') as file:
        data = json.load(file)

    authors = [item['author'] for item in data]
    author_freq = Counter(authors)

    top_authors = author_freq.most_common(n)
    return top_authors

