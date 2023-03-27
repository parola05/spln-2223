import re

'''
    Read the abreviations file and return:
        list of abreviations words
    The abr file have the following format:
        <abr1>
        <abr2>
        ...
        <abrN> 
'''
def parse_abr(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    palavras = []
    for linha in linhas:
        palavras.extend(linha.split())

    return palavras

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
    Change each <abr> to <#abr#>
'''
def changeAbr(content,lang=None,abrFile=None):
    if abrFile != None:
        # abr used is the user's file
        abrs = parse_abr(abrFile)
        for abr in abrs:
            content = re.sub(abr + '\.', '#' + abr + '#', content)
            content = re.sub(abr.capitalize() + '\.', '#' + abr.capitalize() + '#', content)
    elif lang:
        # abr used is the default language file
        abrs = parse_abr("default_abreviations/" + lang + ".txt")
        for abr in abrs:
            content = re.sub(abr + '\.', '#' + abr + '#', content)
            content = re.sub(abr.capitalize() + '\.', '#' + abr.capitalize() + '#', content)

    return content

'''
    Change each <#abr#> to <abr>
'''
def recoverAbr(content,lang=None,abrFile=None):
    if abrFile != None:
        # abr used is the user's file
        abrs = parse_abr(abrFile)
        for abr in abrs:
            content = re.sub('#' + abr + '#', abr + '.', content)
            content = re.sub('#' + abr.capitalize() + '#', abr.capitalize() + '.', content)
    elif lang:
        # abr used is the default language file
        abrs = parse_abr("default_abreviations/" + lang + ".txt")
        for abr in abrs:
            content = re.sub('#' + abr + '#', abr + '.', content)
            content = re.sub('#' + abr.capitalize() + '#', abr.capitalize() + '.', content)

    return content 

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