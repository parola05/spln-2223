import spacy
import re


class AddressShield():

    social_networks_regex = {
        r"(https?://)?(?:www\.)?(?:facebook\.com|fb\.com).*": "Facebook...",
        r"(https?://)?(?:www\.)?(?:twitter\.com|twttr\.com).*": "Twitter...",
        r"(https?://)?(?:www\.)?(instagram\.com|instagr\.am).*": "Instagram...",
        r"(https?://)?(?:www\.)?(?:linkedin\.com|lnkd\.in).*": "LinkedIn...",
        r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be).*": "YouTube...",
        r"(https?://)?(?:www\.)?(?:t\.me|telegram\.me).*": "Telegram...",
        r"(https?://)?(?:www\.)?(?:api\.)?(?:whatsapp\.com|wa\.me).*": "WhatsApp...",
        r"(https?://)?(?:www\.)?(?:tiktok\.com|vm\.tiktok\.com).*": "TikTok...",
        r"(https?://)?(?:www\.)?(?:pinterest\.[a-z]{2,3}|pinimg\.com).*": "Pinterest...",
        r"(https?://)?(?:www\.)?(?:reddit\.com|redd\.it).*": "Reddit...",
        r"(https?://)?(?:www\.)?(?:[a-zA-Z0-9_\-]+\.tumblr\.com).*": "Tumblr...",
        r"(https?://)?(?:www\.)?flickr\.com.*": "Flickr...",
        r"(https?://)?(?:www\.)?quora\.com.*": "Quora...",
        r"(https?://)?(?:www\.)?medium\.com.*": "Medium...",
        r"(https?://)?(?:www\.)?twitch\.tv.*": "Twitch...",
        r"(https?://)?(?:www\.)?zoom\.us.*": "Zoom...",
        r"(https?://)?meet.google.com.*": "Google Meet...",
        r"(https?://)?(?:www\.)?(?:meet\.jit\.si|jitsi\.(?:org|app)).*": "Jitsi...",
        r"(https?://)?(?:www\.)?trello\.com.*": "Trello...",
        r"(https?://)?(?:[a-z0-9]+\.){0,1}slack\.com.*": "Slack...",
        r"(https?://)?(?:www\.)?(?:discord\.gg|discord(?:app)?)\.com.*": "Discord...",
        r"(https?://)?(?:[a-z]+\.)?stack(?:exchange)\.com.*": "Stack Exchange...",
        r"(https?://)?(?:[a-z]+\.)?stack(?:overflow)\.com.*": "Stack Overflow...",
        r"(https?://)?(?:[a-z]+\.)?stack(?:apps)\.com.*": "Stack Apps...",
        r"(https?://)?(?:www\.)?github\.com.*": "GitHub...",
        r"(https?://)?(?:www\.)?gitlab\.com.*": "GitLab...",
        r"(https?://)?(?:www\.)?goodreads\.com.*": "Goodreads...",
    }

    address_regex = [
        r"n(([u|ú]m)?e(ro)?)?º?\.?\s?\d+",
        r"\d{4}-\d{2,3}-?",
        r"[,;:-]",
        r"((Piso|Andar)\s?\d*)|(RC|R/C|r(é|e)s(-|\s)do(-|\s)ch(ã|a)o)|(Cave)|(Sótão)|(Sobreloja)|(Loja)|(Subcave)|(Sobreloja)|(Sótão)|(Subcav)"
    ]

    def __init__(self, text) -> None:
        self.text = text
        self.nlp = spacy.load("pt_core_news_sm")

    def check_context(self, doc: spacy.__doc__, i: int) -> bool:
        if i == 0:
            return False
        if self.match_address(doc[i-1].text) or self.match_address(doc[i+1].text):
            return True
        if doc[i + 1].ent_type_ == "LOC" or doc[i + 1].ent_type_ == "GPE":
            return True

    def match_address(self, text: str) -> bool:
        for item in self.address_regex:
            if re.search(item, text, re.IGNORECASE):
                return True
        return False

    def shield(self) -> str:
        '''
        description:
            Anonymize "addresses data":
            - home address;
            - email;
            - web addresses;
            - social network addresses.
        return:
            Anonymized self.text
        '''
        doc = self.nlp(self.text)
        replace_loc = False
        anonymized_text = ""
        prev_token_space = False
        for (i, token) in enumerate(doc):
            if replace_loc:
                if (re.match(r"(\d+|em|na|no)", token.text)):
                    if (self.check_context(doc, i)):
                        continue
                elif (
                    token.ent_type_ == "LOC"
                    or token.ent_type_ == "GPE"
                    or self.match_address(token.text)
                ):
                    continue
                else:
                    replace_loc = False
            if token.like_email:
                if prev_token_space:
                    anonymized_text += " "
                anonymized_text += "email..."
            elif token.like_url:
                url_matched = False
                if prev_token_space:
                    anonymized_text += " "
                for pattern, replacement in self.social_networks_regex.items():
                    if re.match(pattern, token.text, re.IGNORECASE):
                        anonymized_text += replacement
                        url_matched = True
                        break
                if not url_matched:
                    anonymized_text += "www..."
            elif token.ent_type_ == "LOC" or token.ent_type_ == "GPE":
                if not replace_loc:
                    replace_loc = True
                    if prev_token_space:
                        anonymized_text += " "
                    anonymized_text += "localização..."
            else:
                if prev_token_space:
                    anonymized_text += " "
                anonymized_text += token.text
            prev_token_space = bool(token.whitespace_)

        return anonymized_text.strip()


text = \
    """ 
Era uma bela manhã de verão, quando o José Pedro decidiu que iria
visitar a Rua da Chãozinha, nº25, 1º andar, em Lisboa. Isto deveu-se ao
anúncio que ele encontrou em www.facebook.com. Inicialmente, o José
Pedro ainda visitou o vídeo presente em www.youtube.com para verificar a
veracidade dos factos apresentados no anúncio. Como parecia tudo muito
bom, dirigiu-se a www.google.com, para aceder ao seu email. Lá, enviou
um email para reservas@gmail.com para reservar o seu lugar.
"""

shield = AddressShield(text)
print(shield.shield())
