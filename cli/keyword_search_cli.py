import argparse
import json
import string

with open("data/movies.json") as f:
    movies = json.load(f)["movies"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f'Searching for: {args.query}')

            query = args.query.translate(
                str.maketrans("" , "" , string.punctuation)
            )

            count = 1
            for movie in movies:
                if count == 6:
                    break
                title = movie['title'].translate(
                    str.maketrans("", "", string.punctuation)
                )
                if query.lower() in title.lower():
                    print(f'{count}. {movie['title']}')
                    count += 1
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()