from transformers import T5Tokenizer, T5ForConditionalGeneration, GPT2Tokenizer, GPT2LMHeadModel, pipeline
from story_analyzer.archiver import Archiver
from story_analyzer.book_analyzer import BookAnalyzer

class Book:
    
    def __init__(self, content) -> None:
        self.content = content
        self.gpt_model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.gpt_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.t5_model = T5ForConditionalGeneration.from_pretrained('t5-small', return_dict=True)
        self.t5_tokenizer = T5Tokenizer.from_pretrained('t5-small')


    def quiz(self):
        content_ids = self.gpt_tokenizer.encode(self.content, return_tensors = 'pt')
        
        generated_text_samples = self.gpt_model.generate(
            content_ids,
            max_length= 100,  
            do_sample=True,  
            top_k=100,
            top_p=0.92,
            temperature=0.8,
            repetition_penalty= 1.5,
            num_return_sequences= 6
        )

        fake_texts = []
        for i, beam in enumerate(generated_text_samples):
            fake_texts.append(self.gpt_tokenizer.decode(beam, skip_special_tokens=True))

        return fake_texts

    def translate(self,toLanguage="Germany"):
        input = "Harry Potter said: I want to kill Woldermort! This guy deserves a bad death."
        input_ids = self.t5_tokenizer("translate English to " + toLanguage + ": " + input, return_tensors="pt").input_ids 
        outputs = self.t5_model.generate(input_ids, max_length=10000, num_beams=4)
        decoded = self.t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded

    def saveBook(self):
        language = self.detectLanguage()
        print(language)
        analyzer : BookAnalyzer = BookAnalyzer(language)


    def detectLanguage(self):
        model_ckpt = "papluca/xlm-roberta-base-language-detection"
        pipe = pipeline("text-classification", model=model_ckpt)
        preds = pipe(self.content, top_k=None, truncation=True, max_length=128)
        if preds:
            pred = preds[0]
            return pred["label"]
        else:
            return None



b = Book(content="Harry Potter sagte: Ich will Woldermort töten, dieser Mann verdient einen schlechten Tod.")
b.saveBook()
options = b.quiz()
translation = b.translate()
print(translation)