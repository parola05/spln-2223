import spacy
import re

class NameShield():
    def __init__(self,text) -> None:
        self.text = text

    def shield(self):
        '''
            description: 
                Anonymize "names data":
                    - person names (surname and nicknames)
                    - organization names
            return:
                Anonymized self.text
                    - person names and organization names are changed converted 
                    in their respectives initial letters with a "point" separator character
                        Ex: Henrique Costa -> H.C.
                            Henrique -> H
        '''

        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.text)

        for ent in doc.ents:
            if ent.label_ == "PERSON" or ent.label_ == "ORG":
                ent_names = re.split(r"\s+",ent.text)
                anonymized_name = ".".join(name[0] for name in ent_names) # create new string with the initital letters of entity names separated by "point"
                self.text = re.sub(ent.text,anonymized_name,self.text) # substitue all ocurrences of the entity name by the anonymized text
        
        return self.text
