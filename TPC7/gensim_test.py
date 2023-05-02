from gensim.models import Word2Vec
from gensim.utils import tokenize

book_content = []

with open("livro.txt", "r", encoding="utf-8") as f:
    for line in f:
        book_content.append(list(tokenize(line,lower=True)))

model = Word2Vec(book_content, size=100, window=5, min_count=1, workers=4)

print(model.wv.most_similar('harry'))

model.wv.save_word2vec_format("model_harry")

#python -m gensim.scripts.word2vec2tensor -i model_harry -o model_harry