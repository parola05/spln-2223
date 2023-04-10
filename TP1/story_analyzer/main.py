import argparse
import story_analyzer.get_book as get_book
from story_analyzer.book import Book
import re
import colorama
from colorama import Fore, Style
from story_analyzer.archiver import Archiver
import json


def panic(message):
    print(Fore.RED + f"error: {message}")
    reset = Style.RESET_ALL
    exit(1)

def main():
    args_parser = argparse.ArgumentParser(
        description='Book Analyzer: get insight informations of your storie')
    args_parser.add_argument('input', nargs='?', type=str, metavar='input',
                             help='input file path or book name (only in web mode)')
    args_parser.add_argument('output', nargs=1, type=str,
                             metavar='output', help='output file path. The extension automatic is set to JSON')
    args_parser.add_argument('-m', '--mode', nargs=1, type=str,
                             choices=['local', 'web'], help='app modes', default=['local'])
    args_parser.add_argument(
        '-q', '--quiz', action='store_true', help='quiz game')
    args_parser.add_argument('-t', '--translate', nargs='?', type=str, choices=[
                             'French', 'German', 'Romanian'], help='translate the book', const=['French'])
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
    # TODO add information about which queries will be saved
    args_parser.add_argument('--save', nargs=1, type=str,
                             help='the book will be saved and so will any queries invoked deemed savable.', metavar='title')
    args_parser.add_argument('--read', nargs=1, type=str,
                             help='for queries saved the response time will be quicker, since the query done '
                                  'will be a lookup to a database with the book info. However if a query was not saved or '
                                  'is not deemed savable then the query times will remain the same', metavar='title')
    args_parser.add_argument('-p', '--projection', nargs=1, type=str,
                             help='project queries in the text range. Projetion type is [<bottom>;<higher>]')
    args_parser.add_argument('-sa', '--sentiment_analysis', action='store_true',
                             help="sentiment analysis of the book")
    args_parser.add_argument('-v', '--view', action='store_true',
                             help="view book content. With projection is used, the text is limited by the projection range")
    args_parser.add_argument('-si', '--similar', nargs=1, type=str,
                             help='finds the sentence that better describes the input given. It also gives the word offset'
                                  ' from the beginning of the story. Useful for finding an exact reference.')
    args_parser.add_argument('-sn', '--sentence_no', action='store_true', help='get the number of sentences of a story')


    args = args_parser.parse_args()

    try:
        if args.input:
            book_content = get_book.get_book(args.mode[0], args.input)
            # limit book_content with projection is used
            book = Book(book_content)
            if args.projection and args.input and not args.read:

                pattern = r'\[(\d+):(\d+)\]'
                match = re.search(pattern, str(args.projection[0]))

                if match:
                    bottom_limit = int(match.group(1))
                    higher_limit = int(match.group(2))

                    try:
                        book.setProjection(bottom_limit, higher_limit)
                    except TypeError as e:
                        panic(str(e))
        elif args.read:
            archive = Archiver()
            bookObj = archive.getStory(args.read[0])
            if bookObj and "content" in bookObj.keys():
                book_content = bookObj["content"]
            else:
                panic("There wasn't a save for this title before this reading command")
            book = Book(title=args.read[0])

        out = {}
        saveDict = {}

        if args.sentence_no:
            if args.read and "sentence_no" in bookObj.keys():
                sentence_no = bookObj["sentence_no"]
            else:
                sentence_no = book.spacy_queries.querySentences()
            out["sentence_no"] = sentence_no
            if args.save:
                saveDict["sentence_no"] = sentence_no
        if args.similar:
            _input = args.similar[0]
            similar = book.spacy_queries.similarSentence(_input)
            out["similar"] = similar
        if args.actions:
            # if it's requested a read and the book info is cached then use it else do the query
            if args.read and "actions" in bookObj.keys():
                actions = bookObj["actions"]
            else:
                actions = book.spacy_queries.queryActions(args.actions)
            out["actions"] = actions
            if args.save:
                saveDict["actions"] = actions
        if args.language:
            if args.read and "language" in bookObj.keys():
                language = bookObj["language"]
            else:
                language = book.queryLanguage()
            out["language"] = language
            if args.save:
                saveDict["language"] = language
        if args.quiz:
            if args.read and "sentences" in bookObj.keys():
                quiz_sentences = bookObj["sentences"]
            else:
                quiz_sentences = book.quiz()
            out["sentences"] = quiz_sentences
            if args.save:
                saveDict["sentences"] = quiz_sentences
        if args.translate:
            if args.read and "translation" in bookObj.keys() and (args.translate in bookObj["translation"].keys()):
                translation = bookObj["translation"][args.translate]
            else:
                try:
                    translation = book.translate(args.translate)
                except TypeError as e:
                    panic(str(e))
                
            out["translation"] = translation
            if args.save:
                saveDict["translation"] = {args.translate: translation}
        if args.summary:
            if args.read and "summary" in bookObj.keys():
                summary = bookObj["summary"]
            else:
                summary = book.summarize()
            out["summary"] = summary
            if args.save:
                saveDict["summary"] = summary
        if args.discussions:
            topics = book.topics()
            print(topics)
        if args.characters:
            if args.read and "characters" in bookObj.keys():
                charactersInfo = bookObj["characters"]
            else:
                charactersInfo = book.spacy_queries.getCharacters()
            out["characters"] = charactersInfo
            if args.save:
                saveDict["characters"] = charactersInfo
        if args.sentiment_analysis:
            if args.read and "sentiment" in bookObj.keys():
                sentiment = bookObj["sentiment"]
            else:
                sentiment = book.sentiment()
            out["sentiment"] = sentiment
            if args.save:
                saveDict["sentiment"] = sentiment
            print(book.sentiment())
        if args.view:
            out["view"] = book.content

        with open(args.output[0] + ".json", 'w') as file:
            json.dump(out, file, indent=4)

        if args.save:
            book.saveContent(args.save[0], saveDict)

    except ValueError as e:
        panic(str(e))


if __name__ == "__main__":
    main()
