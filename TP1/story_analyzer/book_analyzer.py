import spacy
import os
from collections import Counter
from typing import List

class ParserModels:
    def __init__(self):
        self.path: str = os.path.dirname(__file__) + "/data/spacy_models"
        self.file = open(self.path, "r", encoding="utf-8")
        self.languages: dict = {}
        for line in self.file.readlines():
            tokens = line.split()
            self.languages[tokens[0]] = tokens[1]


    def getModel(self, language : str) -> str:
        if language not in self.languages.keys():
            return None
        return  self.languages[language]


class BookAnalyzer:
    def __init__(self, language : str, text : str):
        self.parser: ParserModels = ParserModels()
        self.model :str = self.__modelFromLanguage(language)
        self.nlp = spacy.load(self.model)
        self.doc = self.nlp(text)
        self.maxElements = 100

    def __modelFromLanguage(self, language: str) -> str :
        return self.parser.getModel(language)

    def queryActions(self):
        "Gets the most actions of a book"
        verbs: Counter = Counter()
        for w in self.doc:
            if w.pos_ == "VERB":
                verbs[w.lemma_] += 1
        return verbs.most_common(self.maxElements)

    def querySentences(self):
        "Gets the number of sentences of a text"
        return len(self.doc.sents)





