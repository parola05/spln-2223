#!/usr/bin/env python
import sys 
import fileinput 
import argparse
import helpers as hp

parser = argparse.ArgumentParser(description='Processador de linguagem natural')
parser.add_argument("-fl", action="store_true", help="Retorna uma frase por linha")
parser.add_argument("-pl", action="store_true", help="Retorna uma palavra por linha")
parser.add_argument('texto', type=argparse.FileType('r'), help='Arquivo de texto de entrada')

args = parser.parse_args()

text = ''
text = args.texto.read()

def main():
    global text
     
    if args.fl: # Frases por Linha
        text = hp.removeNewLine(text)
        text = hp.changeElipses(text)
        text = hp.changeSrAndSrta(text)
        sentences = hp.getSentences(text)

        for i in range(0,len(sentences)):
            sentences[i] = hp.recoverElipses(sentences[i])
            sentences[i] = hp.recoverSrAndSraAndSrta(sentences[i])

        for sentence in sentences:
            print(sentence)
    elif args.fl: # Palavra por Linha
        pass        
    else:
        pass

if __name__ == "__main__":
    main()