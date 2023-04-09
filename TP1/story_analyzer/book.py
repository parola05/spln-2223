from transformers import T5Tokenizer, T5ForConditionalGeneration, GPT2Tokenizer, GPT2LMHeadModel, PegasusForConditionalGeneration, PegasusTokenizer, pipeline
from story_analyzer.spacy_queries import SpacyQueries
import random
import gensim
from story_analyzer.archiver import Archiver


class Book:

    def __init__(self, content) -> None:
        self.content: str = content
        language_abr, language_long = self.__detectLanguage()
        self.language: str = language_long
        self.spacy_queries: SpacyQueries = SpacyQueries(
            language_abr, self.content)
        self.db : Archiver = Archiver()

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
            fake_sentences.append(gpt_tokenizer.decode(
                beam, skip_special_tokens=True))

        # put the true sentence in a random position
        random_index = random.randint(0, len(fake_sentences))
        fake_sentences.insert(random_index, random_sentence)

        return fake_sentences

    def translate(self, toLanguage="Germany"):
        "translate the book content"

        print("Translate " + self.language + " to " + toLanguage)

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

        print(lda_model.print_topics())

    def saveContent(self, title : str, archiveDict : dict):
        self.db.addStory(title, archiveDict)

    def getContent(self, title : str):
        return self.db.getStory(title)

    # TODO: too many tokens for this model, need to find a way (maybe split text in chunks and analyze each chunk, then merge results (average?))
    def sentiment(self) -> str:
        pipe = pipeline("sentiment-analysis")
        result = pipe(self.content)
        if result:
            return result[0]["label"]
        else:
            return "neutral"

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
