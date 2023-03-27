#!/usr/bin/env python
"""Processador de linguagem natural!""" 
import argparse
from .helpers import *

__version__ = "0.8"

def main():
    parser = argparse.ArgumentParser(description='Processador de linguagem natural')
    parser.add_argument("--fl", action="store_true", help="Retorna uma frase por linha")
    parser.add_argument("--pl", action="store_true", help="Retorna uma palavra por linha")
    parser.add_argument("--pag", type=int, help="Retorna o conteúdo da página fornecida")
    parser.add_argument("--abr", type=str, help="Ficheiro de abreviações do utilizador")
    parser.add_argument("--lang", type=str, help="Especificação da língua do texto")
    parser.add_argument('texto', type=argparse.FileType('r'), help='Arquivo de texto de entrada ... LOBE')

    args = parser.parse_args()

    text = ''
    text = args.texto.read()
     
    if args.fl: # Frases por Linha
        text = removeNewLine(text)
        text = changeElipses(text)
        if args.abr:
            text = changeAbr(content=text,abrFile=args.abr)
        elif args.lang:
            text = changeAbr(content=text,lang=args.lang)
        else:
            text = changeAbr(content=text,lang="en")
        sentences = getSentences(text)

        for i in range(0,len(sentences)):
            sentences[i] = recoverElipses(sentences[i])
            if args.abr:
                sentences[i] = recoverAbr(content=sentences[i],abrFile=args.abr)
            elif args.lang:
                sentences[i] = recoverAbr(content=sentences[i],lang=args.lang)
            else:
                sentences[i] = recoverAbr(content=sentences[i],lang="en")

        for sentence in sentences:
            print(sentence)
            pass
    elif args.pl: # Palavra por Linha
        words = getWords(text)

        for word in words:
            print(word)   
    elif args.pag: # Conteúdo da uma página
        content = getContentByPage(text,args.pag)
        print("Page " + str(args.pag) + ":\n")
        print(content)
    else:
        pass

if __name__ == "__main__":
    main()