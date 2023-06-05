class DocumentShield():
    def __init__(self,text) -> None:
        self.text = text

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