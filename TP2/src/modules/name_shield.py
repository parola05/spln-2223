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
        '''
        return self.text
