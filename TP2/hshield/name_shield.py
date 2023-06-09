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

        nlp = spacy.load('pt_core_news_md')
        doc = nlp(self.text)

        dic_names = {} # anonymized_names -> [name1,name2,...,nameN]

        for ent in doc.ents:
            if ent.label_ == "PER" or ent.label_ == "ORG":
                
                ent_names = re.split(r"\s+",ent.text)
                anonymized_name = ".".join(name[0] for name in ent_names) # create new string with the initital letters of entity names separated by "point"
                
                # check if the name has the anonymized_name equals to others entities
                id = 0
                if anonymized_name in dic_names:
                    # anonymized_name already have been used by some entity(s)

                    if ent.text in dic_names[anonymized_name]:
                        # anonymized_name already have been used by the entity -> get the id of this entity (id is the position in the list)
                        id = dic_names[anonymized_name].index(ent.text)
                    else:
                        # anonymized_name never was used by the entitity -> id is the last position of the list
                        id = len(dic_names[anonymized_name])
                        dic_names[anonymized_name].append(ent.text)
                else:
                    # anonymized_name never was used by any entity -> id is 0 (first position)
                    dic_names[anonymized_name] = [ent.text]

                anonymized_name += '('+str(id)+')' # add id to anonymized name
                self.text = re.sub(ent.text,anonymized_name,self.text) # substitue all ocurrences of the entity name by the anonymized text
        
        return self.text
