import spacy
from collections import Counter
from typing import List
import random
from story_analyzer.parser_models import ParserModels
from sortedcontainers.sortedset import SortedSet

class SpacyQueries:
    # The goal of this class is to encapsulate all the spacy queries that are
    # done with the same text and same model
    def __init__(self, language : str, text : str):
        self.parser: ParserModels = ParserModels()
        self.model :str = self.__modelFromLanguage(language)
        self.text = text
        self.docReady = False

    def __createDoc(self):
        self.nlp = spacy.load(self.model)
        self.doc = self.nlp(self.text)
        self.docReady = True

    def __modelFromLanguage(self, language: str) -> str :
        return self.parser.getModel(language)

    def __createOne(self):
        if not self.docReady:
            self.__createDoc()

    def getStopWords(self):
        return self.nlp.Defaults.stop_words

    def queryActions(self, top : int):
        "Gets the most actions of a book"
        # Acts as a singleton
        self.__createOne()
        verbs: Counter = Counter()
        for w in self.doc:
            if w.pos_ == "VERB":
                verbs[w.lemma_] += 1
        return verbs.most_common(top)

    def querySentences(self):
        "Gets the number of sentences of a text"
        # Acts as a singleton
        self.__createOne()
        return len(self.doc.sents)

    def queryGetRandomSentence(self):
        "Gets a random sentence of a text. The random setence must have more than 20 tokens"
        self.__createOne()
        random_sentence = random.choice(list(self.doc.sents))
        while len(random_sentence) < 20:
            random_sentence = random.choice(list(self.doc.sents))
        return random_sentence

    def similarSentence(self, input : str) -> (str, int):
        "Given a summary of a sentence it returns the actual sentence and the offset where it is present"
        # Acts as a singleton
        self.__createOne()
        #requires that the language of the input is the same
        search_sent = self.nlp(input)

        search_no_stop_words = self.nlp(' '.join([str(word) for word in search_sent if not word.is_stop]))

        simSet = SortedSet(key=lambda x: x[1])

        for sent in self.doc.sents:
            sent_no_stop_words = self.nlp(' '.join([str(word) for word in sent if not word.is_stop]))
            entry = (sent.text, search_no_stop_words.similarity(sent_no_stop_words), sent.start)
            simSet.add(entry)

        return simSet[0]

    def getCharacters(self):
        "Get characters information of a book"
        
        # Acts as a singleton
        self.__createOne()
        
        characters = {}

        for sent in self.doc.sents:
            for ent in sent.ents:
                if ent.label_ == "PERSON":
                    name = ent.text.lower().strip()
                    characters[name] = characters.get(name, 0) + 1
        
        return characters
    