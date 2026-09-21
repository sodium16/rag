import string
from search_utils import DEFAULT_SEARCH_LIMIT, STOPWORDS_PATH, load_movies
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text) -> None:
        token_list = tokenize_text(text)
        for token in token_list:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_documents(self, term) -> list[int]:
        return sorted(self.index[term])

    def build() -> None:
        movies = load_movies()
        for movie in movies:


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