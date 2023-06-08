import spacy
import re
import math

class DocumentShield():
    def __init__(self, text) -> None:
        self.window = None
        self.window_pos_max = None
        self.window_pos = None
        self.window_size = None

        self.text = text
        self.nlp = spacy.load("pt_core_news_md")
        self.doc = self.nlp(self.text)

        self.init_window()

    def init_window(self):
        self.window_pos = 0
        self.window_pos_max = len(self.doc) - 1
        self.window_size = min(self.window_pos_max, 10)
        self.window = []

        for (i, token) in enumerate(self.doc):
            self.window.append(token)
            if i == self.window_size - 1:
                break

    def window_text(self):
        list_text = [token.lemma_ + " " for token in self.window]
        return "".join(list_text)
    def slide_right(self, offset):
        token = self.get_token(offset)
        self.window_pos = token
        half_size = self.window_size/2
        if token - half_size < 0:
            lower_bound = 0
            excess = token - half_size
            upper_bound = token + half_size + (- excess)
        elif token + half_size > self.window_pos_max:
            upper_bound = self.window_pos_max
            excess = token + half_size - self.window_pos_max
            lower_bound = token - half_size - excess
        else:
            lower_bound = math.trunc(token - half_size)
            upper_bound = math.trunc(token + half_size)

        self.window = self.doc[lower_bound:upper_bound]

    def get_token(self, offset):
        for i, token in enumerate(self.doc[self.window_pos:]):
            if token.idx <= offset < token.idx + len(token.text):
                return i + self.window_pos

    def change(self, match):
        "For test purposes to see the effeects of the sliding window"
        print("MATCH")
        self.slide_right(match.start(0))
        print(self.window_text())
        return "NUMERO " + str(self.window_pos)
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
        self.text = re.sub("número", self.change, self.text)
        print(self.text)

        return self.text
