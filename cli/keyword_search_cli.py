import argparse
from keyword_search import search_command, build_command, tf_command, idf_command, tfidf_command

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")
    build_parser = subparsers.add_parser("build", help="Builds the search index")
    tf_parser = subparsers.add_parser("tf", help="run term frequency tests")
    tf_parser.add_argument('doc_id', type=int, help="Enter the document id")
    tf_parser.add_argument('term', type=str, help='enter a term to search')
    idf_parser = subparsers.add_parser("idf", help="search via idf")
    idf_parser.add_argument("term", type=str, help = 'term to search for')
    tfidf_parser = subparsers.add_parser('tfidf', help='get the tfidf score')
    tfidf_parser.add_argument('doc_id', type=int, help='Enter the document id')
    tfidf_parser.add_argument('term', type=str, help='Enter a term to search')
    args = parser.parse_args()

    match args.command:
        case "search":
            print('Searching for:', args.query)
            movies = search_command(args.query)
            for i, movie in enumerate(movies, 1):
                print(f"{i}. {movie['title']}")
        case "build":
            print("Building inverted index...")
            build_command()
            print("Built inverted index successfully")
        case "tf":
            tf = tf_command(args.doc_id, args.term)
            print(f"Term frequency of {args.term} in document {args.doc_id} is {tf}")
        case "idf":
            idf = idf_command(args.term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")
        case "tfidf":
            tf_idf = tfidf_command(args.doc_id, args.term)
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf:.2f}")
        case _:
            parser.print_help()
    

if __name__ == "__main__":
    main()