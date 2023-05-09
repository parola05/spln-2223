import argparse 
from gensim.models import Word2Vec

parser = argparse.ArgumentParser(
    prog="Cria Modelo",
    epilog="Made for SPLN 2022/2023"
)

parser.add_argument('model')
parser.add_argument('--analogias','-a',default="./val.txt")

args = parser.parse_args()
modelArg = args.model 
input = args.analogias

model = Word2Vec.load(modelArg)

fd = open(input,"r")

for line in fd:
    words = line.split()
    if len(words) == 3:
        w1,w2,w3 = words
        model.wv.most_similar(positive=words[w1,w2],negative=words[w3])