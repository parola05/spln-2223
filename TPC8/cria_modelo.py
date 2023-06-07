import argparse 
from glob import glob 
from gensim.models import Word2Vec
from gensim.utils import tokenize

parser = argparse.ArgumentParser(
    prog="Cria Modelo",
    epilog="Made for SPLN 2022/2023"
)

parser.add_argument('dir')
parser.add_argument('--out','-o',default=".")
parser.add_argument('--epochs','-e',default=5)
parser.add_argument('--dim','-d',default=100)

args = parser.parse_args()

dir = args.dir 
epochs = args.epochs
dim = args.dim 
out = args.out

files = glob(f'{dir}\\*.txt')

cont = []
for file in files:
    fd = open(file,"r") 
    for line in fd:
        cont.append(list(tokenize(line,lowercase=True)))

model = Word2Vec(cont,size=dim)
model.wv.save_word2vec_format(out + "model")