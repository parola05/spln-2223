import os

import spacy
from spacy.cli import download

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
        try:
            spacy.load(self.languages[language])
        except:
            download(self.languages[language])

        return self.languages[language]
