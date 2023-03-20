import re

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