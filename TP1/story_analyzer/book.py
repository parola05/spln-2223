
from transformers import T5Tokenizer, T5ForConditionalGeneration, GPT2Tokenizer, GPT2LMHeadModel, PegasusForConditionalGeneration, PegasusTokenizer, pipeline, AutoModelForSequenceClassification, AutoTokenizer, logging
from story_analyzer.spacy_queries import SpacyQueries
import torch
import random
import gensim
from story_analyzer.archiver import Archiver
from typing import Optional
from story_analyzer.parser_models import ParserModels
import spacy

class Book:

    def __init__(self, content: Optional[str]=None, title: Optional[str] = None) -> None:
        logging.set_verbosity_error()
        self.db : Archiver = Archiver()
        if content:
            self.content: str = content
            self.read_only: bool = False
            language_abr, language_long = self.__detectLanguage()
            self.language: str = language_long
            self.language_abr = language_abr
            self.spacy_queries: SpacyQueries = SpacyQueries(
                language_abr, self.content)
        elif title:
            bookObj: dict = self.db.getStory(title)
            # These fields are always stored when a save is done
            if bookObj["content"] and bookObj["language"]:
                self.content = bookObj["content"]
                self.language = bookObj["language"]
                self.language_abr = bookObj["language_abr"]
            else:
                raise Exception('A save was not previously done')

            self.spacy_queries: SpacyQueries = SpacyQueries(title=title)
            self.read_only: bool = True

        self.device = 0 if torch.cuda.is_available() else -1

    def quiz(self):
        "Generate a quiz game with six false sentences and one true sentence. The goal is the user guess the true sentence"

        # get a random true sentence from the text
        random_sentence = self.spacy_queries.queryGetRandomSentence()

        # load GPT model and tokenizer
        gpt_model = GPT2LMHeadModel.from_pretrained('gpt2')
        gpt_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        # encode the first 5 words from the sentence to put in the model
        content_ids = gpt_tokenizer.encode(
            str(random_sentence[0:5]), return_tensors='pt')

        # generate six fake sentences
        generated_text_samples = gpt_model.generate(
            content_ids,
            max_length=50,
            do_sample=True,
            top_k=100,
            top_p=0.92,
            temperature=0.8,
            repetition_penalty=1.5,
            num_return_sequences=6
        )

        # decode fake sentences
        fake_sentences = []
        for beam in generated_text_samples:
            fake_sentences.append(str(gpt_tokenizer.decode(
                beam, skip_special_tokens=True)))

        # put the true sentence in a random position
        random_index = random.randint(0, len(fake_sentences))
        fake_sentences.insert(random_index, str(random_sentence))

        return fake_sentences

    def translate(self, toLanguage="Germany"):
        "translate the book content"

        if len(self.content) > 512:
            raise TypeError("The text are to long to be translated. Try a little one.")

        # load t5 model and tokenizer
        t5_model = T5ForConditionalGeneration.from_pretrained(
            't5-small', return_dict=True)
        t5_tokenizer = T5Tokenizer.from_pretrained(
            't5-small', model_max_length=10000)

        # encode text to put in the model
        input_ids = t5_tokenizer("translate " + self.language + "to " +
                                 toLanguage + ": " + self.content, return_tensors="pt").input_ids

        # generate the translated content
        outputs_ids = t5_model.generate(
            input_ids, max_length=10000, num_beams=4)

        # decode translated text
        translation = t5_tokenizer.decode(
            outputs_ids[0], skip_special_tokens=True)

        return translation

    def summarize(self):
        "summarize the book content"

        if len(self.content) > 1024:
            raise TypeError("The text are to long to be translated. Try a little one.")

        # load Pegasus model and tokenizer
        pegasus_model = PegasusForConditionalGeneration.from_pretrained(
            'google/pegasus-cnn_dailymail')
        pegasus_tokenizer = PegasusTokenizer.from_pretrained(
            'google/pegasus-cnn_dailymail')

        # encode text to put in the model
        input_ids = pegasus_tokenizer(
            self.content, truncation=True, padding="longest", return_tensors='pt')

        # generate the summary content
        output_ids = pegasus_model.generate(**input_ids)

        # decode summary text
        summary = pegasus_tokenizer.batch_decode(output_ids[0])

        return ' '.join(summary)

    def topics(self):
        "get most relevant discussions from the book"

        # get stop words from space_queries
        stop_words = self.spacy_queries.getStopWords()

        data_words = gensim.utils.simple_preprocess(self.content, deacc=True)
        bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)

        def remove_stopwords(texts):
            return [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in stop_words] for doc in
                    texts]

        def make_bigrams(texts):
            return [bigram_mod[doc] for doc in texts]

        def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
            texts_out = []
            for sent in texts:
                parser = ParserModels()
                model = parser.getModel(self.language_abr)
                nlp = spacy.load(model)
                doc = nlp(" ".join(sent))
                texts_out.append(
                    [token.lemma_ for token in doc if token.pos_ in allowed_postags])
            return texts_out

        data_words_nostops = remove_stopwords(data_words)
        data_words_bigrams = make_bigrams(data_words_nostops)
        data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=[
                                        'NOUN', 'ADJ', 'VERB', 'ADV'])

        id2word = gensim.corpora.Dictionary(data_lemmatized)
        texts = data_lemmatized
        corpus = [id2word.doc2bow(text) for text in texts]

        lda_model = gensim.models.ldamodel.LdaModel(
            corpus=corpus,
            id2word=id2word,
            num_topics=15,
            random_state=100,
            update_every=1,
            chunksize=100,
            passes=10,
            alpha='auto',
            per_word_topics=True
        )

        return lda_model.print_topics()

    def saveContent(self, title : str, archiveDict : dict):
        #works because self.language is not used to init spacy queries and nor is the archive used for that
        archiveDict.update({"content": self.content, "language": self.language, "language_abr": self.language_abr})
        self.db.addStory(title, archiveDict)
        self.spacy_queries.saveDoc(title)

    def getContent(self, title : str):
        return self.db.getStory(title)

    def sentiment(self) -> str:
        model = AutoModelForSequenceClassification.from_pretrained(
            "bert-base-multilingual-uncased")
        tokenizer = AutoTokenizer.from_pretrained(
            "bert-base-multilingual-uncased")
        pipe = pipeline("sentiment-analysis", model=model,
                        tokenizer=tokenizer, device=self.device)

        chunks = self.content.split(".")

        labels = {"Neutral": 0, "Positive": 0, "Negative": 0}

        dataset = [{"text": text} for text in chunks]

        results = pipe(dataset, batch_size=8)

        for result in results:
            label = result["label"]
            if label == "LABEL_0":
                labels["Negative"] += 1
            elif label == "LABEL_1":
                labels["Positive"] += 1
            else:
                labels["Neutral"] += 1

        return max(labels, key=labels.get)

    def __detectLanguage(self) -> str:
        model_ckpt = "papluca/xlm-roberta-base-language-detection"
        pipe = pipeline("text-classification", model=model_ckpt)
        preds = pipe(self.content, top_k=None, truncation=True, max_length=128)
        if preds:
            pred = preds[0]
            # if this method is called then it stores in a instance variable
            language_long = ''
            if (pred["label"] == "es"):
                language_long = "Spanish"
            elif (pred["label"] == "en"):
                language_long = "English"
            elif (pred["label"] == "de"):
                language_long = "German"
            elif (pred["label"] == "it"):
                language_long = "Italian"
            elif (pred["label"] == "pt"):
                language_long = "Portuguese"
            elif (pred["label"] == "fr"):
                language_long = "French"

            return pred["label"], language_long
        else:
            return None

    def queryLanguage(self) -> str:
        return self.language

    def setProjection(self,bottom,higher):
        self.content = self.spacy_queries.querySentencesInRange(bottom=bottom,higher=higher)