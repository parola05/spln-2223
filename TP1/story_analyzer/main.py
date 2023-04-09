import argparse
import story_analyzer.get_book as get_book
from story_analyzer.book import Book
import re
import colorama
from colorama import Fore, Style
import json

from story_analyzer.archiver import Archiver


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
    args_parser.add_argument('-si', '--similar', nargs=1, type=str,
                             help='finds the sentence that better describes the input given. It also gives the word offset'
                                  ' from the beginning of the story. Useful for finding an exact reference.')
    args_parser.add_argument('-sn', '--sentence_no', action='store_true', help='get the number of sentences of a story')


    args = args_parser.parse_args()

    try:
        book_content = get_book.get_book(args.mode[0], args.input[0])

        out = {}
        saveDict = {}
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

        if args.sentence_no:
            if args.read and (sentence_no := book.getContent(args.read[0])["sentence_no"]):
                pass
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
            if args.read and (actions := book.getContent(args.read[0])["actions"]):
                pass
            else:
                actions = book.spacy_queries.queryActions(args.actions)
            out["actions"] = actions
            if args.save:
                saveDict["actions"] = actions
        if args.language:
            if args.read and (language := book.getContent(args.read[0])["language"]):
                pass
            else:
                language = book.queryLanguage()
            out["language"] = language
            if args.save:
                saveDict["language"] = language
        if args.quiz:
            quiz_sentences = book.quiz()
            out["sentences"] = quiz_sentences
        if args.translate:
            if args.read and book.getContent(args.read[0])["translation"] and (args.translate in book.getContent(args.read[0])["translation"].keys()):
                translation = book.getContent(args.read[0])["translation"][args.translate]
            else:
                translation = book.translate(args.translate)
            out["translation"] = translation
            if args.save:
                saveDict["translation"] = {args.translate: translation}
        if args.summary:
            if args.read and (summary := book.getContent(args.read[0])["summary"]):
                pass
            else:
                summary = book.summarize()
            out["summary"] = summary
            if args.save:
                saveDict["summary"] = summary
        if args.discussions:
            topics = book.topics()
            # TODO put in the output file
        if args.characters:
            if args.read and (charactersInfo := book.getContent(args.read[0])["characters"]):
                pass
            else:
                charactersInfo = book.spacy_queries.getCharacters()
            out["characters"] = charactersInfo
            if args.save:
                saveDict["characters"] = charactersInfo
        if args.sentiment_analysis:
            if args.read and (sentiment := book.getContent(args.read[0])["sentiment"]):
                pass
            else:
                sentiment = book.sentiment()
            out["sentiment"] = sentiment
            if args.save:
                saveDict["sentiment"] = sentiment
            print(book.sentiment())

        with open(args.output[0] + ".json", 'w') as file:
            json.dump(out, file, indent=4)

        if args.save:
            book.saveContent(args.save[0], saveDict)



    except ValueError as e:
        panic(str(e))


if __name__ == "__main__":
    main()
