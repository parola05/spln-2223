import spacy
import os
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
    def __init__(self, language : str):
        self.parser: ParserModels = ParserModels()
        self.model :str = self.__modelFromLanguage(language)
        self.nlp = spacy.load(self.model)

    def __modelFromLanguage(self, language: str) -> str :
        return self.parser.getModel(language)

