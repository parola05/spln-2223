import argparse
import get_book
from story_analyzer.book import Book
from story_analyzer.spacy_queries import SpacyQueries

def panic(message):
    print(f"error: {message}")  # todo: colors / warnings vs errors
    exit(1)  # change if warning

def main():
    args_parser = argparse.ArgumentParser(description='Book Analyzer: get insight informations of your storie')
    args_parser.add_argument('input', nargs=1, type=str, metavar='input', help='input file path or book name (only in web mode)')
    args_parser.add_argument('output', nargs=1, type=str,metavar='output', help='output file path')
    args_parser.add_argument('-m', '--mode', nargs=1, type=str, choices=['local', 'web'], help='app modes', default=['local'])
    args_parser.add_argument('-q', '--quiz', action='store_true', help='quiz game')
    args_parser.add_argument('-t', '--translate', nargs='?', type=str, choices=['English', 'Portuguese', 'Germany'], help='translate the book', const=['English'])
    args_parser.add_argument('-d', '--discussions', action='store_true', help='list the book discussions (topics)')
    args_parser.add_argument('-s', '--summary', action='store_true', help='summarize the book')
    args_parser.add_argument('-l', '--language', action='store_true', help='detect book language')
    args_parser.add_argument('-a', '--actions', nargs='?', type=int, help='get the top most actions of a book', const=10)
    args_parser.add_argument('--save', nargs=1, type=str, help='the book will be saved and so will any queries invoked deemed savable.', metavar='title')

    args = args_parser.parse_args()

    try:
        book_content = get_book.get_book(args.mode[0],args.input[0])

        book = Book(book_content)

        if args.actions:
           print("I'm here")
           book.spacy_queries.queryActions(args.actions)
        if args.language:
            print(book.language())
        elif args.quiz:

            true_phrase, fake_phrases = book.quiz()

            print("0:", true_phrase)
            for phrase, i in enumerate(fake_phrases):
                print(i,":",str(phrase))

        elif args.translate:
            print(book.translate(args.translate[0]))

        elif args.summary:
            print(book.summary())

        elif args.discussions:
            print(book.topics())

    except ValueError as e:
        panic(str(e))

if __name__ == "__main__":
    main()