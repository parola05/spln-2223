class AddressShield():
    def __init__(self, text) -> None:
        self.text = text
        self.nlp = spacy.load("pt_core_news_sm")

    def shield(self) -> str:
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
        doc = self.nlp(self.text)
        anonymized_text = []
        for token in doc:
            if token.like_email:
                anonymized_text.append("email...")
            elif token.like_url:
                if re.search(r"facebook\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("Facebook...")
                elif re.search(r"twitter\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("Twitter...")
                elif re.search(r"instagram\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("Instagram...")
                elif re.search(r"linkedin\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("LinkedIn...")
                elif re.search(r"youtube\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("YouTube...")
                elif re.search(r"whatsapp\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("WhatsApp...")
                elif re.search(r"t\.me", token.text, re.IGNORECASE):
                    anonymized_text.append("Telegram...")
                elif re.search(r"tiktok\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("TikTok...")
                elif re.search(r"pinterest\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("Pinterest...")
                elif re.search(r"tumblr\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("Tumblr...")
                elif re.search(r"reddit\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("Reddit...")
                elif re.search(r"twitch\.tv", token.text, re.IGNORECASE):
                    anonymized_text.append("Twitch...")
                elif re.search(r"spotify\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("Spotify...")
                elif re.search(r"soundcloud\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("SoundCloud...")
                elif re.search(r"medium\.com", token.text, re.IGNORECASE):
                    anonymized_text.append("Medium...")
                else:
                    anonymized_text.append("www...")
            elif token.ent_type_ == "LOC" or token.ent_type_ == "GPE":
                anonymized_text.append("localização...")
            else:
                anonymized_text.append(token.text)

        self.text = " ".join(anonymized_text)
        return self.text
