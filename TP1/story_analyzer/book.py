from transformers import T5Tokenizer, T5ForConditionalGeneration, GPT2Tokenizer, GPT2LMHeadModel, PegasusForConditionalGeneration, PegasusTokenizer, pipeline
from archiver import Archiver
from spacy_queries import SpacyQueries
import spacy
import random
import gensim

class Book:
    
    def __init__(self, content) -> None:
        self.content = content
        #For a harrypotter book it takes around 1sec.
        #Since a lot of functions require a language input
        #for choosing which models to import it's better to
        #always calculate this query straight away.
        self.language = self.__detectLanguage()


    def quiz(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.content)
        sentences = list(doc.sents)

        random_phrase = random.choice(sentences)
        while len(random_phrase) < 8:
            random_phrase = random.choice(sentences)

        print("radom:",random_phrase)

        gpt_model = GPT2LMHeadModel.from_pretrained('gpt2')
        gpt_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        
        content_ids = gpt_tokenizer.encode(random_phrase, return_tensors = 'pt')
        
        generated_text_samples = gpt_model.generate(
            content_ids,
            max_length= 200,  
            do_sample=True,  
            top_k=100,
            top_p=0.92,
            temperature=0.8,
            repetition_penalty= 1.5,
            num_return_sequences= 6
        )

        fake_texts = []
        for i, beam in enumerate(generated_text_samples):
            fake_texts.append(gpt_tokenizer.decode(beam, skip_special_tokens=True))

        return random_phrase, fake_texts

    def translate(self,toLanguage="Germany"):
        t5_model = T5ForConditionalGeneration.from_pretrained('t5-small', return_dict=True)
        t5_tokenizer = T5Tokenizer.from_pretrained('t5-small')
        input_ids = t5_tokenizer("translate English to " + toLanguage + ": " + self.content, return_tensors="pt").input_ids 
        outputs_ids = t5_model.generate(input_ids, max_length=10000, num_beams=4)
        translation = t5_tokenizer.decode(outputs_ids[0], skip_special_tokens=True)
        return translation


    def summarize(self):
        pegasus_model = PegasusForConditionalGeneration.from_pretrained('google/pegasus-cnn_dailymail')
        pegasus_tokenizer = PegasusTokenizer.from_pretrained('google/pegasus-cnn_dailymail')
        input_ids = pegasus_tokenizer(self.content, truncation=True, padding="longest", return_tensors='pt')
        output_ids = pegasus_model.generate(**input_ids)
        summary = pegasus_tokenizer.batch_decode(output_ids[0])
        return ' '.join(summary)

    def saveBook(self):
        pass

    def __detectLanguage(self) -> str:
        model_ckpt = "papluca/xlm-roberta-base-language-detection"
        pipe = pipeline("text-classification", model=model_ckpt)
        preds = pipe(self.content, top_k=None, truncation=True, max_length=128)
        if preds:
            pred = preds[0]
            #if this method is called then it stores in a instance variable
            self.language = pred["label"]
            return pred["label"]
        else:
            return None

    def queryLanguage(self) -> str:
        return self.language
    def topics(self):
        nlp = spacy.load("en_core_web_sm")

        stop_words = nlp.Defaults.stop_words
        data_words = gensim.utils.simple_preprocess(self.content, deacc=True)
        bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
        trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        def remove_stopwords(texts):
            return [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in stop_words] for doc in
                    texts]

        def make_bigrams(texts):
            return [bigram_mod[doc] for doc in texts]

        def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
            texts_out = []
            for sent in texts:
                doc = nlp(" ".join(sent))
                texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
            return texts_out

        data_words_nostops = remove_stopwords(data_words)
        data_words_bigrams = make_bigrams(data_words_nostops)
        data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

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