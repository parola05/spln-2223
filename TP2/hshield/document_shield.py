import spacy
import re

class DocumentShield():
    def __init__(self,text) -> None:
        self.text = text
        self.nlp = spacy.load("pt_core_news_md")
        self.doc = self.nlp(self.text)
        self.window = self.init_window(15, text)
        self.window_text = "".join(self.window)
        self.window_pos = 0
        self.window_pos_max = len(self.doc)

    def init_window(self, size, text):
        window = []
        for (i, token) in enumerate(self.doc):
            window.append(token.lemma_ + " ")
            if i == size:
                break
        return window

    def slide_right(self):
        pass

    def shield(self):
        '''
            description: 
                Anonymize "documents data":
                    - passport number;
                    - driving license;
                    - Telephone number;
                    - NIF;
                    - CC
                    ...
            return:
                Anonymized self.text
        '''
        return self.text
