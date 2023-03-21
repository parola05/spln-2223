#!/usr/bin/env python
"""Processador de linguagem natural!"""
import sys 
import fileinput 
import argparse
import sys
import re

__version__ = "0.3"

def main():
    '''
    Remove '\n' from the input text
    '''
    def removeNewLine(text):
        text = re.sub('\n', ' ', text)
        return text 

    '''
        Change '...' by '#3P#'
    '''
    def changeElipses(text):
        text = re.sub('\.\.\.', '#3P#', text)
        return text 

    '''
        Change '#3P#' by '...'
    '''
    def recoverElipses(text):
        text = re.sub('#3P#', '...', text)
        return text 

    '''
        Change 'Sr.' by '#Sr#' and 'Srta.' by '#Srta#'
    '''
    def changeSrAndSrta(text):
        text = re.sub('Sr\.', '#Sr#', text)
        text = re.sub('Sra\.', '#Sra#', text)
        text = re.sub('Srta\.', '#Srta#', text)
        return text 

    '''
        Change '#Sr#' by 'Sr.' and '#Srta# by 'Srta.'
    '''
    def recoverSrAndSraAndSrta(text):
        text = re.sub('#Sr#', 'Sr.', text)
        text = re.sub('#Sra#', 'Sra.', text)
        text = re.sub('#Srta#', 'Srta.', text)
        return text 

    '''
        Get sentences from text
        Obs: expect '...', '\n', 'Srta.' and 'Sr.' previous processed
        Return: list of sentences
    '''
    def getSentences(text):
        sentences = re.split(r"\.\s", text)
        return sentences

    '''
        Get content of a given page
        Obs: a new page is identified by two '\n' in sequence
        Obs(2): expect previous treatment of title and subtitle of chapters (that have two '\n' in sequence too)
    '''
    def getContentByPage(text,page):
        sentences = re.split(r"\n\n", text)
        return sentences[page]

    '''
        Get words from text
        Obs: expect all pontuations treated early
        Return: list of words
    '''

    def getWords(text):
        words = re.split(r"\s", text)
        return words

    parser = argparse.ArgumentParser(description='Processador de linguagem natural')
    parser.add_argument("--fl", action="store_true", help="Retorna uma frase por linha")
    parser.add_argument("--pl", action="store_true", help="Retorna uma palavra por linha")
    parser.add_argument("--pag", type=int, help="Retorna o conteúdo da página fornecida")
    parser.add_argument('texto', type=argparse.FileType('r'), help='Arquivo de texto de entrada')

    args = parser.parse_args()

    text = ''
    text = args.texto.read()
     
    if args.fl: # Frases por Linha
        text = removeNewLine(text)
        text = changeElipses(text)
        text = changeSrAndSrta(text)
        sentences = getSentences(text)

        for i in range(0,len(sentences)):
            sentences[i] = recoverElipses(sentences[i])
            sentences[i] = recoverSrAndSraAndSrta(sentences[i])

        for sentence in sentences:
            print(sentence)
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