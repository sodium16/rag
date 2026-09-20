import string
from search_utils import DEFAULT_SEARCH_LIMIT, load_movies

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
    return text.translate(str.maketrans("", "", string.punctuation))

def tokenize_text(text : str) -> str:
    preprocessed_text = preprocess_text(text)
    text_tokens = preprocessed_text.split()
    res = []
    for text_token in text_tokens:
        if text_token:
            res.append(text_token)
    return res

def has_token(query_tokens : list[str], title_tokens : list[str]) -> bool:
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False