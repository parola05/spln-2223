class Dic_concept():
    def __init__(self, concepts):
        self.concepts = concepts 

    def toHtml(self, outputFile):

        htmlPage = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8"/>
                <title>Dicionário orientado ao conceito</title>
            </head>
            <body>
        '''
        for concept in self.concepts:
            htmlPage = htmlPage + '''
                <h1>''' + str(concept.index) + '''</h1>
                <h2>Áreas</h2>
                <ul>
                '''
            for area in concept.areas:
                htmlPage = htmlPage  + '''
                    <li>''' + area.name + '''</li>
                '''
                    
            htmlPage = htmlPage + '''
                </ul> 
                <h2>Línguas</h2>
            '''

            for language in concept.languages:
                htmlPage = htmlPage  + '''
                <h3>''' + language.name + '''</h3>
                '''
                for synonym in language.synonyms:
                    htmlPage = htmlPage  + '''
                <h4>''' + synonym.name + '''</h4>
                '''
                    if not synonym.atribs == None:
                        for atrib in synonym.atribs:
                            htmlPage = htmlPage  + '''
                <p>''' + atrib.name + ''': ''' + atrib.value + '''</p>
                '''

        htmlPage = htmlPage + f'''
                </body>
            </html>
            '''
        f = open(outputFile + ".html", "w")
        f.write(htmlPage)
        f.close()   

class Concept():
    def __init__(self, index, areas, languages):
        self.index = index 
        self.areas = areas 
        self.languages = languages

class Area:
    def __init__(self, name):
        self.name = name 

class Language():
    def __init__(self, name, synonyms):
        self.name = name 
        self.synonyms = synonyms  

class Synoyms():
    def __init__(self, name, atribs):
        self.name = name 
        self.atribs = atribs 

class Atribute():
    def __init__(self, name, value):
        self.name = name 
        self.value = value 