import spacy
import os
from collections import Counter
from typing import List
import gensim
from story_analyzer.parser_models import ParserModels
from sortedcontainers.sortedset import SortedSet

class SpacyQueries:
    # The goal of this class is to encapsulate all the spacy queries that are
    # done with the same text and same model
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


    def similarSentence(self, input : str) -> (str, int):
        "Given a summary of a sentence it returns the actual sentence and the offset where it is present"
        #requires that the language of the input is the same
        search_sent = self.nlp(input)

        search_no_stop_words = self.nlp(' '.join([str(word) for word in search_sent if not word.is_stop]))

        simSet = SortedSet(key=lambda x: x[1])

        for sent in self.doc.sents:
            sent_no_stop_words = self.nlp(' '.join([str(word) for word in sent if not word.is_stop]))
            entry = (sent.text, search_no_stop_words.similarity(sent_no_stop_words), sent.start)
            simSet.add(entry)

        return simSet[0]