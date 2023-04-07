import argparse
import get_book
from book import Book

def panic(message):
    print(f"error: {message}")  # todo: colors / warnings vs errors
    exit(1)  # change if warning

def main():
    
    args_parser = argparse.ArgumentParser(description='Book Analyzer: get insight informations of your storie')
    args_parser.add_argument('input', nargs=1, type=str, metavar='input', help='input file path or book name (only in web mode)')
    args_parser.add_argument('output', nargs=1, type=str,metavar='output', help='output file path')
    args_parser.add_argument('-m', '--mode', nargs=1, type=str, choices=['local', 'web'], help='app modes', default=['local'])
    args_parser.add_argument('-q', '--quiz', action='store_true', help='quiz game')
    args_parser.add_argument('-t', '--translate', nargs=1, type=str, choices=['English', 'Portuguese', 'Germany'], help='translate the book', default=['English'])
    args_parser.add_argument('-d', '--discussions', action='store_true', help='list the book discussions (topics)')
    args_parser.add_argument('-s', '--summary', action='store_true', help='summarize the book')
    args_parser.add_argument('-l', '--language', action='store_true', help='detect book language')

    args = args_parser.parse_args()

    try:
        book_content = get_book.get_book(args.mode[0],args.input[0])
        book = Book(book_content)

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