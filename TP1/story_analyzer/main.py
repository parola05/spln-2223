import argparse
import get_book
from book import Book
import re
import colorama
from colorama import Fore, Style
import json

def panic(message):
    print(Fore.RED + f"error: {message}")
    reset = Style.RESET_ALL
    exit(1)

def main():
    args_parser = argparse.ArgumentParser(
        description='Book Analyzer: get insight informations of your storie')
    args_parser.add_argument('input', nargs=1, type=str, metavar='input',
                             help='input file path or book name (only in web mode)')
    args_parser.add_argument('output', nargs=1, type=str,
                             metavar='output', help='output file path. The extension automatic is set to JSON')
    args_parser.add_argument('-m', '--mode', nargs=1, type=str,
                             choices=['local', 'web'], help='app modes', default=['local'])
    args_parser.add_argument(
        '-q', '--quiz', action='store_true', help='quiz game')
    args_parser.add_argument('-t', '--translate', nargs='?', type=str, choices=[
                             'English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese'], help='translate the book', const=['English'])
    args_parser.add_argument(
        '-d', '--discussions', action='store_true', help='list the book discussions (topics)')
    args_parser.add_argument(
        '-s', '--summary', action='store_true', help='summarize the book')
    args_parser.add_argument(
        '-l', '--language', action='store_true', help='detect book language')
    args_parser.add_argument('-c', '--characters', action='store_true',
                             help='get informations of the book characters')
    args_parser.add_argument('-a', '--actions', nargs='?', type=int,
                             help='get the top most actions of a book', const=10)
    args_parser.add_argument('--save', nargs=1, type=str,
                             help='the book will be saved and so will any queries invoked deemed savable.', metavar='title')
    args_parser.add_argument('-p', '--projection', nargs=1, type=str,
                             help='project queries in the text range. Projetion type is [<bottom>;<higher>]')
    args = args_parser.parse_args()

    try:
        book_content = get_book.get_book(args.mode[0], args.input[0])

        # limit book_content with projection is used
        if args.projection:

            pattern = r'\[(\d+):(\d+)\]'
            match = re.search(pattern, str(args.projection[0]))

            if match:
                bottom_limit = int(match.group(1))
                higher_limit = int(match.group(2))
                bottom_limit = int((bottom_limit * len(book_content)) / 100)
                higher_limit = int((higher_limit * len(book_content)) / 100)
                book_content = book_content[bottom_limit:higher_limit]

        book = Book(book_content)

        if args.actions:
            actions = book.spacy_queries.queryActions(args.actions)
            with open(args.output[0] + ".json", 'w') as file:
                 json.dump({"actions": actions}, file, indent=4)
        elif args.language:
            language = book.queryLanguage()
            with open(args.output[0] + ".json", 'w') as file:
                 json.dump({"language": language}, file, indent=4)
        elif args.quiz:
            quiz_sentences = book.quiz()
            with open(args.output[0] + ".json", 'w') as file:
                 json.dump({"sentences": quiz_sentences}, file, indent=4)
        elif args.translate:
            translation = book.translate(args.translate)
            with open(args.output[0] + ".json", 'w') as file:
                 json.dump({"translation": translation}, file, indent=4)
        elif args.summary:
            summary = book.summarize()
            with open(args.output[0] + ".json", 'w') as file:
                 json.dump({"summary": summary}, file, indent=4)
        elif args.discussions:
            topics = book.topics()
            # TODO put in the output file
        elif args.characters:
            charactersInfo = book.spacy_queries.getCharacters()
            with open(args.output[0] + ".json", 'w') as file:
                 json.dump(charactersInfo, file, indent=4)

    except ValueError as e:
        panic(str(e))

if __name__ == "__main__":
    main()
