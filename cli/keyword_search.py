import string
from search_utils import (DEFAULT_SEARCH_LIMIT, STOPWORDS_PATH, load_movies, CACHE_DIR)
from nltk.stem import PorterStemmer
from pickle import dump, load
import os
import math
from collections import defaultdict, Counter

stemmer = PorterStemmer()

class InvertedIndex:
    def __init__(self):
        #token to indexes
        self.index = defaultdict(set)
        #indexes to movies
        self.docmap = {}
        #term to its count
        self.term_frequencies = defaultdict(Counter)
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")
        self.tf_path = os.path.join(CACHE_DIR, "term_frequencies.pkl")

    def __add_document(self, doc_id, text) -> None:
        token_list = tokenize_text(text)
        for token in token_list:
            self.term_frequencies[doc_id][token]+=1
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
        with open(self.tf_path, 'wb') as f:
            dump(self.term_frequencies, f)
            
    def load(self) -> None:
        with open(self.index_path, 'rb') as f:
            self.index = load(f)
        with open(self.docmap_path, 'rb') as f:
            self.docmap = load(f)
        with open(self.tf_path, 'rb') as f:
            self.term_frequencies = load(f)
            
    def get_tf(self, doc_id, term) -> int :
        if term in self.term_frequencies[doc_id]:
            return self.term_frequencies[doc_id][term]
        return 0
    
def tokenize_term(term : str) -> str:
    texts = tokenize_text(term)
    if len(texts) != 1:
        raise ValueError("Contains multiple tokens")
    return texts[0]

def tf_command(doc_id, term) -> int:
    index = InvertedIndex()
    term = tokenize_term(term)
    index.load()
    return index.get_tf(doc_id, term)

def idf_command(term) -> float:
    index = InvertedIndex()
    index.load()
    term = tokenize_term(term)
    total_doc_count = len(index.docmap)
    term_match_doc_count = len(index.get_documents(term))
    return math.log((total_doc_count + 1) / (term_match_doc_count + 1))

def build_command():
    index = InvertedIndex()
    index.build()
    index.save()
    

def search_command(query : str, limit : int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    results, seen = [], set()
    index = InvertedIndex()
    try:
        index.load()
    except FileNotFoundError:
        print("index files not found, please build index first")
        return []
    query_vec = tokenize_text(query)
    for q in query_vec:
        if(q in index.index):
            ids = index.get_documents(q)
            for id in ids:
                if id not in seen:
                    seen.add(id)
                    results.append(index.docmap[id]) 
                    if(len(results) >=5):
                        return results
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

# def has_token(query_tokens : list[str], title_tokens : list[str]) -> bool:
#     for query_token in query_tokens:
#         for title_token in title_tokens:
#             if query_token in title_token:
#                 return True
#     return False