class AddressShield():
    def __init__(self,text) -> None:
        self.text = text

    def shield(self):
        '''
            description: 
                Anonymize "addresses data":
                    - home address
                    - email;
                    - web addresses;
                    - social network addresses;
            return:
                Anonymized self.text
        '''
        return self.text