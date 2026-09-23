import string
from search_utils import (DEFAULT_SEARCH_LIMIT, STOPWORDS_PATH, load_movies, CACHE_DIR)
from nltk.stem import PorterStemmer
from pickle import dump
import os
from collections import defaultdict

stemmer = PorterStemmer()

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
        self.docmap = {}
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")

    def __add_document(self, doc_id, text) -> None:
        token_list = tokenize_text(text)
        for token in token_list:
            self.index[token].add(doc_id)

    def get_documents(self, term) -> list[int]:
        return sorted(self.index[term])

    def build(self) -> None:
        movies = load_movies()
        for movie in movies:
            self.docmap[movie["id"]] = movie
            self.__add_document(movie['id'], f"{movie['title']} {movie['description']}")

    def save(self) -> None:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(self.index_path, 'wb') as f:
            dump(self.index, f)
        with open(self.docmap_path, 'wb') as f:
            dump(self.docmap, f)

def build_command():
    index = InvertedIndex()
    index.build()
    index.save()
    docs = index.get_documents('merida')
    print(f"First document for token 'merida' = {docs[0]}")


def search_command(query : str, limit : int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    for movie in movies:
        query_tokens = tokenize_text(query)
        title_tokens = tokenize_text(movie["title"])
        if has_token(query_tokens, title_tokens):
            results.append(movie)
            if len(results) >= limit:
                break 
    return results

def preprocess_text(text : str) -> str:
    text = text.lower()
    #remove punctuation (what to replace, what to replace with, what to remove)
    return text.translate(str.maketrans("", "", string.punctuation))

def load_stopwords() -> list[str]:
    with open(STOPWORDS_PATH, 'r') as f:
        return [preprocess_text(word) for word in f.read().splitlines()]

stopwords = load_stopwords()

def tokenize_text(text : str) -> list[str]:
    preprocessed_text = preprocess_text(text)
    text_tokens = preprocessed_text.split()
    ans = []
    for text_token in text_tokens:
        if text_token not in stopwords:
            ans.append(stemmer.stem(text_token))
    return ans

def has_token(query_tokens : list[str], title_tokens : list[str]) -> bool:
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False