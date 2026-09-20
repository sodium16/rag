import string
from search_utils import DEFAULT_SEARCH_LIMIT, load_movies

def search_command(query : str, limit : int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    for movie in movies:
        preprocessed_query = preprocess_text(query)
        preprocessed_title = preprocess_text(movie["title"])
        query_vec = preprocessed_query.split()
        for word in query_vec:
            if word in preprocessed_title:
                results.append(movie)
                if len(results) >= limit:
                    return results
    
    return results

def preprocess_text(text : str) -> str:
    text = text.lower()
    return text.translate(str.maketrans("", "", string.punctuation))