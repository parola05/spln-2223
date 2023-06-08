import spacy
import re
import math
import os

class DocumentShield():
    def __init__(self, text) -> None:
        self.window = None
        self.window_pos_max = None
        self.window_pos = None
        self.window_size = None
        self.cur_dict = None

        self.expressions = self.parse()
        self.text_original = text
        self.text = text
        self.nlp = spacy.load("pt_core_news_md")
        self.doc = self.nlp(self.text)
        self.delta_history = []


        self.cur_match = None
        self.init_window()

    def parse(self):
        path = os.path.dirname(__file__) + "/data/regex_doc.txt"
        file = open(path, "r")
        country = ""
        match = ""
        last_empty = True
        res = {}
        keys = ["regex", "keywords", "check", "sub"]
        for line in file:
            line = line.strip()
            split = line.split(':')
            if split[0] != '':
                if last_empty:
                    if split[0] == "country":
                        country = split[1]
                        res[country] = {}
                    else:
                        match = split[0]
                        res[country][match] = {}
                    last_empty = False
                elif split[0] in keys:
                    key = split[0]
                    if key == "keywords":
                        value = split[1].split(',')
                    elif key == "check":
                        value = split[1] == "yes"
                    else:
                        value = split[1]

                    res[country][match][key] = value
            else:
                last_empty = True

        import json
        #print(json.dumps(res, indent=2))
        #with open('filename', 'w', encoding='utf8') as json_file:
        #    json.dump(res, json_file, ensure_ascii=False, indent=2)
        return res

    def init_window(self):
        self.window_pos = 0
        self.window_pos_max = len(self.doc) - 1
        self.window_size = min(self.window_pos_max, 15)
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

    def keywords_present(self, keywords):
        for key in keywords:
            doc_word = self.nlp(key)
            lemma_list = [w.lemma_ + " " for w in doc_word]
            key_norm = "".join(lemma_list).strip()
            window_norm = self.window_text().strip()
            if re.search(key_norm, window_norm):
                return True
        return False

    def update_pos_deltas(self, index, new_delta):
        res = []
        for (char_pos, delta) in self.delta_history[index:]:
            res.append((char_pos + new_delta, delta))

        return res

    def put_delta_char(self, char_start, new_delta):
        for i,(char_pos, delta) in enumerate(self.delta_history):
            if char_pos > char_start:
                self.delta_history[i:] = self.update_pos_deltas(i, new_delta)
                self.delta_history.insert(i, (char_start, new_delta))
                return
        self.delta_history.append((char_start, new_delta))


    def original_pos(self, match_pos):
        res = match_pos
        for (pos, delta) in self.delta_history:
            if pos < match_pos:
                res -= delta
        return res

    def change(self, match):
        "For test purposes to see the effeects of the sliding window"
        original_pos = self.original_pos(match.start(0))
        self.cur_match = match.group(0)
        self.slide_right(original_pos)
        if not self.cur_dict["check"] and self.keywords_present(self.cur_dict["keywords"]):
            sub = self.cur_dict["sub"]
            self.put_delta_char(match.start(0), len(sub) - len(match.group(0)))
            return sub
        else:
            return match.group(0)

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
        #para já assumir só uma linguagem
        #no futuro é possível para cada linguagem fazer uma análise
        #com o spacy com diferentes linguagens.
        for match, dict in self.expressions["pt"].items():
            self.cur_dict = dict
            self.text = re.sub(dict["regex"], self.change, self.text)
            # Ao substituir os regexes o text original muda e o get_token deixa
            # de funcionar como devido à posição de chars não combinar
            # Acho que dá para otimizar isto
            self.init_window()

        print(self.text)

        return self.text
