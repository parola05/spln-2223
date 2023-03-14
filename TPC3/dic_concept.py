class Dic_concept():
    def __init__(self, concepts):
        self.concepts = concepts 

    def toHtml(self, outputFile):

        htmlPage = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8"/>
                <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
                <title>Dicionário orientado ao conceito</title>
            </head>
            <body>
            <div class="w3-card">
            <header class="w3-container w3-blue">
                <h1>Dicionário orientado ao conceito</h1>
            </header>
                <ul class="w3-ul">
        '''
        for concept in self.concepts:
            htmlPage = htmlPage + '''
                <li>
                    <h1>''' + str(concept.index) + '''</h1>
                    <h2>Áreas</h2>
                    <ul class="w3-ul">
                '''
            for area in concept.areas:
                htmlPage = htmlPage  + '''
                        <li>''' + area.name + '''</li>
                '''
                    
            htmlPage = htmlPage + '''
                    </ul> 
                    <h2>Línguas</h2>
                    <ul class="w3-ul">
            '''

            for language in concept.languages:
                htmlPage = htmlPage  + '''
                    <li>
                    <h3>''' + language.name + '''</h3>
                    <ul class="w3-ul">
                '''
                for synonym in language.synonyms:
                    htmlPage = htmlPage  + '''
                    <li>
                    <h4>''' + synonym.name + '''</h4>
                    <ul class="w3-ul">
                '''
                    if not synonym.atribs == None:
                        for atrib in synonym.atribs:
                            htmlPage = htmlPage  + '''<li>
                    <p>''' + atrib.name + ''': ''' + atrib.value + '''</p>
                    </li>
                '''
                    htmlPage = htmlPage + '''</ul>'''
                htmlPage = htmlPage + '''
                </ul>
                '''
            htmlPage = htmlPage + '''
                </ul>
            '''

        htmlPage = htmlPage + f'''
                        </ul>
                    </div> 
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