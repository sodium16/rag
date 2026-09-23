import json
import os
from typing import Any, TypedDict

class Movie(TypedDict):
    id: int
    title: str
    description:str

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")

DEFAULT_SEARCH_LIMIT = 5

def load_movies() -> list[Movie]:
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    return data['movies']

def load_stopwords() -> list[str]:
    with open(STOPWORDS_PATH, 'r') as f:
        stopwords = f.read().splitlines()
    return stopwords