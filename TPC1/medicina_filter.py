import re
import json

texto = open('medicina.xml', 'r', encoding="utf-8").read()

###################### Conversão para a Língua Intermédia

def remove_header_footer(texto):
    texto = re.sub(r'<text.* font="1">ocabulario.*</text>', r'###', texto)
    texto = re.sub(r'.*\n###\n.*\n', r'___', texto)
    texto = re.sub(r'<page.*\n|</page>\n', r'', texto)
    
    return texto

texto = remove_header_footer(texto)

def marcaE(texto):
    texto = re.sub(r'<text.* font="3"><b>\s*(\d+)\s*(\w+(?: \w+)*)\s*(\w)\s*</b></text>\n?', r'\n###IDENT \1;\2;\3', texto)
    texto = re.sub(r'<text.* font="3"><b>\s*(\S.*)</b></text>\n?', r'\n###REM \1', texto)
  
    return texto

texto = marcaE(texto)

def marcaLinguas(texto):
    texto = re.sub(r'<text.* font="0">\s*(es|en|pt|la)\s*</text>\n?', r'\n###TRAD \1 ',texto)

    return texto 

texto = marcaLinguas(texto)

def areaTematicaReplace(m):
    text = '\n###AT '
    for group in m.groups():
        if group != None:
            text += group + ';'
    return text

def marcaAreaTematica(texto):
    texto = re.sub(r'<text.* font="6"><i>\s*(\w+(?: \w+)*)\s*(\w+(?: \w+)*)*</i></text>\n?',areaTematicaReplace,texto)
    return texto 

texto = marcaAreaTematica(texto)

def marcaRedirecionamentoRemissivo(texto):
    texto = re.sub(r'<text.* font="5">\s*Vid.- (.*)</text>\n?',r'\n###RED \1',texto)
    return texto     

texto = marcaRedirecionamentoRemissivo(texto)

def marcaSINouVAR(texto):
    texto = re.sub(r'<text.* font="5">\s*(SIN|VAR).- (.*)</text>\n?',r'\n###\1 \2 ',texto)
    texto = re.sub(r'<text.* font="5">\s*(\S.*)\s*</text>\n?',r'\1 ',texto)
    return texto 

texto = marcaSINouVAR(texto)

def marcaTraducoes(texto):
    texto = re.sub(r'<text.* font="7"><i>\s*(\S.*)\s*</i></text>\n?',r'\1',texto)
    texto = re.sub(r'<text.* font="0">\s*;\s*</text>\n?',r';',texto)
    return texto

texto = marcaTraducoes(texto)

def marcaNota(texto):
    texto = re.sub(r'<text.* font="9">\s*Nota\.- (.*)</text>\n?',r'\n###NOTA \1',texto)
    texto = re.sub(r'<text.* font="9">\s*(\S.*)</text>\n?',r'\1',texto)
    return texto

texto = marcaNota(texto)

def limpaXMLAMais(texto):
    texto = re.sub(r'<text.*>.*</text>\n',r'',texto)
    texto = re.sub(r'<\?xml version="1.0" encoding="UTF-8"\?>\n',r'',texto)
    texto = re.sub(r'<!DOCTYPE pdf2xml SYSTEM "pdf2xml.dtd">\n',r'',texto)
    texto = re.sub(r'<fontspec.*/>\n',r'',texto)
    texto = re.sub(r'<pdf2xml producer="poppler" version="22.02.0">\n',r'',texto)
    return texto 

texto = limpaXMLAMais(texto)

###################### Parser da Língua Intermédia

medicinaConceitos = {}
medicinaConceitos["entradasCompletas"] = []
medicinaConceitos["entradasRemissivas"] = []

def getECIndex(cabecalhoMatch):
    if cabecalhoMatch != None:
        return cabecalhoMatch.split(";")[0]

def getECDenominacao(cabecalhoMatch):
    if cabecalhoMatch != None:
        return cabecalhoMatch.split(";")[1]

def getECCategoriaGramatical(cabecalhoMatch):
    if cabecalhoMatch != None:
        return cabecalhoMatch.split(";")[2]

def getECAreasTematicas(areasTematicasMatch):
    if areasTematicasMatch != None:
        return areasTematicasMatch.split(";")[:-1]
    else:
        return []

def getECSinonimos(sinonimosMatch):
    if sinonimosMatch != None:
        return sinonimosMatch.split(";")
    else:
        return []

def getECVariantes(variantesMatch):
    if variantesMatch != None:
        return variantesMatch.split(";")
    else:
        return []
    
def getECTraducoes(traducoesMatch):
    if traducoesMatch != None:        
        return traducoesMatch.split(";")
    else:
        return []

def getECNota(notaMatch):
    return notaMatch

def preencherEstrutura(texto):
    global i
    entradaCompleta = r'###IDENT (?P<cabecalho>.*)\n###AT (?P<areasTematicas>.*)\n(?:###SIN (?P<SIN>.*)\n)?(?:###VAR (?P<VAR>.*)\n)?(###TRAD es (?P<es>.*)\n)?(###TRAD en (?P<en>.*)\n)?(###TRAD pt (?P<pt>.*)\n)?(###TRAD la (?P<la>.*)\n)?(###NOTA (?P<nota>.*)\n)?'
    entradaRemissiva = r'###REM (?P<rem>.*)\n###RED (?P<red>.*)'

    # parser das entradas completas
    for ec in re.finditer(entradaCompleta,texto):
        ecObj = {}
        
        ecObj["ecIndex"] = getECIndex(ec.groupdict()["cabecalho"])
        ecObj["denominacao"] = getECDenominacao(ec.groupdict()["cabecalho"])
        ecObj["categoriaGramatical"] = getECCategoriaGramatical(ec.groupdict()["cabecalho"])
        ecObj["areasTematicas"] = getECAreasTematicas(ec.groupdict()["areasTematicas"])
        ecObj["sinonimos"] = getECSinonimos(ec.groupdict()["SIN"])
        ecObj["variantes"] = getECVariantes(ec.groupdict()["VAR"])
        ecObj["traducoes"] = {}
        ecObj["traducoes"]["es"] = getECTraducoes(ec.groupdict()["es"])
        ecObj["traducoes"]["en"] = getECTraducoes(ec.groupdict()["en"])
        ecObj["traducoes"]["pt"] = getECTraducoes(ec.groupdict()["pt"])
        ecObj["traducoes"]["la"] = getECTraducoes(ec.groupdict()["la"])
        ecObj["nota"] = getECNota(ec.groupdict()["nota"])

        medicinaConceitos["entradasCompletas"].append(ecObj)

    # parser das entradas remissivas
    for er in re.finditer(entradaRemissiva,texto):
        erObj = {}
        erObj["denominacao"] = er.groupdict()["rem"]
        erObj["referência"] = er.groupdict()["red"]

        medicinaConceitos["entradasRemissivas"].append(erObj)

preencherEstrutura(texto)

with open("medicina.json", "w") as outfile:
    json.dump(medicinaConceitos,outfile,indent=8,ensure_ascii=False)

file = open('medicina.text', 'w')
file.write(texto)