import spacy
import re


class AddressShield():

    social_networks_regex = {
        r"https?://(?:www\.)?(?:facebook\.com|fb\.com)/(?:pages?/[a-zA-Z0-9_.-]+|groups?/[a-zA-Z0-9_.-]+|[^/]+/[a-zA-Z0-9_.-]+)(?:/\d+)?": "Facebook...",
        r"https?://(?:www\.)?(?:twitter\.com|twttr\.com)/[a-zA-Z0-9_]{1,15}(?:/status/\d+)?(?:\?s=\d+)?(?:&s=\d+)?(?:#\w+)?": "Twitter...",
        r"r'https?://(?:www\.)?(?:instagram\.com|instagr\.am)/(?:[a-zA-Z0-9_]{1,30}|p|tv|reel|explore/tags)/[a-zA-Z0-9_\-./]+": "Instagram...",
        r"https?://(?:www\.)?(?:linkedin\.com|lnkd\.in)/(?:in|company)/[a-zA-Z0-9_\-]+(?:/[^/]+)?": "LinkedIn...",
        r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:channel/|user/|c/)?[a-zA-Z0-9\-_]{1,}": "YouTube...",
        r"https?://(?:www\.)?(?:t\.me|telegram\.me)/(?:joinchat/|addstickers/|(?:[cC]/)?)([a-zA-Z0-9_]+)": "Telegram...",
        r"https?://(?:www\.)?(?:api\.)?(?:whatsapp\.com|wa\.me)/(?:send\?phone=)?(\d+)(?:&text=.+)?": "WhatsApp...",
        r"https?://(?:www\.)?(?:tiktok\.com|vm\.tiktok\.com)/(?:[a-zA-Z0-9\-_]+)/?": "TikTok...",
        r"https?://(?:www\.)?(?:pinterest\.[a-z]{2,3}|pinimg\.com)/(?:[^/]+/)*(?:[a-zA-Z0-9\-_]{3,})/?": "Pinterest...",
        r"https?://(?:www\.)?(?:reddit\.com|redd\.it)/(?:r/[^/]+/comments/|user/|u/)?([a-zA-Z0-9_]{3,})/?": "Reddit...",
        r"https?://(?:www\.)?(?:[a-zA-Z0-9_\-]+\.tumblr\.com)/(?:post/)?(\d+)/?": "Tumblr...",
        r"https?://(?:www\.)?flickr\.com/photos/(?:[^/]+/)?(\d+)/?": "Flickr...",
        r"https?://(?:www\.)?quora\.com/(?:profile/[^/]+|question/(\d+))/?(?:\?.*)?": "Quora...",
        r"https?://(?:www\.)?medium\.com/(?:@[^/]+/)?([^/]+)/?(?:\?.*)?": "Medium...",
        r"https?://(?:www\.)?twitch\.tv/([^/]+)/(?:v/(\d+)|clip/([^/]+))/?(?:\?.*)?": "Twitch...",
        r"https?://(?:www\.)?zoom\.us/(?:j/)?(?:my/)?(\d+)(?:\?pwd=[^&]+)?": "Zoom...",
        r"https?://meet.google.com/(\w{3}-\w{4}-\w{3})": "Google Meet...",
        r"https?://(?:www\.)?(?:meet\.jit\.si|jitsi\.(?:org|app))/([^/?]+)": "Jitsi...",
        r"https?://(?:www\.)?trello\.com/(?:c|b|[^/]+)/([^/?]+)": "Trello...",
        r"https?://(?:[a-z0-9]+\.){0,1}slack\.com/(?:[a-z0-9_-]+/){0,1}([^/?]+)": "Slack...",
        r"https?://(?:www\.)?(?:discord\.gg|discord(?:app)?\.com/invite)/([a-zA-Z0-9]+)": "Discord...",
        r"https?://(?:[a-z]+\.)?stack(?:exchange)\.com/(?:q(?:uestions)?|a(?:nswers)?|users)/([^/?#]+)": "Stack Exchange...",
        r"https?://(?:[a-z]+\.)?stack(?:overflow)\.com/(?:q(?:uestions)?|a(?:nswers)?|users)/([^/?#]+)": "Stack Overflow...",
        r"https?://(?:[a-z]+\.)?stack(?:apps)\.com/(?:q(?:uestions)?|a(?:nswers)?|users)/([^/?#]+)": "Stack Apps...",
        r"https?://(?:www\.)?github\.com/([^/?#]+)": "GitHub...",
        r"https?://(?:www\.)?gitlab\.com/([^/?#]+)": "GitLab...",
        r"https?://(?:www\.)?goodreads\.com/(?:book/show|author/show|user/show)/(\d+)": "Goodreads...",
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
                    if re.search(pattern, token.text, re.IGNORECASE):
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
