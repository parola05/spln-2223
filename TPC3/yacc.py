import sys
import ply.yacc as yacc
from lex import tokens
import dic_concept as dc 

def p_dicionario(p):
    "dicionario : conceitos"
    parser.dic = dc.Dic_concept(p[1])
    parser.dic.toHtml("dic")

def p_conceitos(p):
    "conceitos : conceito SEPARADOR1 conceitos"
    p[0] = [p[1]] + p[3]

def p_conceitos_single(p):
    "conceitos : conceito"
    p[0] = [p[1]]

def p_conceito(p):
    "conceito : identidadeconceito SEPARADOR2 AREAS SEPARADOR3 areas SEPARADOR2 LINGUAS SEPARADOR3 linguas"
    p[0] = dc.Concept(p[1],p[5],p[9])

def p_identidadeconceito(p):
    "identidadeconceito :  INDEX"
    p[0] = int(p[1])

def p_areas(p):
    "areas : area SEPARADOR3 areas"
    p[0] = [p[1]] + p[3]

def p_areas_one(p):
    "areas : area"
    p[0] = [p[1]]

def p_area(p):
    "area : NOME"
    p[0] = dc.Area(p[1])

def p_linguas(p):
    "linguas : lingua SEPARADOR3 linguas"
    p[0] = [p[1]] + p[3]

def p_linguas_single(p):
    "linguas : lingua"
    p[0] = [p[1]]

def p_lingua(p):
    "lingua : identidadelingua SEPARADOR4 sinonimos"
    p[0] = dc.Language(p[1], p[3])

def p_identidadelingua(p):
    "identidadelingua : IDENTIDADELINGUA"
    p[0] = p[1]

def p_sinonimos(p):
    "sinonimos : sinonimo SEPARADOR4 sinonimos"
    p[0] = [p[1]] + p[3]

def p_sinonimos_single(p):
    "sinonimos : sinonimo"
    p[0] = [p[1]]

def p_sinonimo(p):
    "sinonimo : NOME SEPARADOR5 atributos"
    p[0] = dc.Synoyms(p[1],p[3])

def p_sinonimo_single(p):
    "sinonimo : NOME"
    p[0] = dc.Synoyms(p[1],None)

def p_atributos(p):
    "atributos : atributo SEPARADOR5 atributos"
    p[0] = [p[1]] + p[3]

def p_atributos_single(p):
    "atributos : atributo"
    p[0] = [p[1]]

def p_atributo(p):
    "atributo : idatrib SEPARADOR6 NOME"
    p[0] = dc.Atribute(p[1], p[3])

def p_idatrib_categoria(p):
    "idatrib : CATEGORIA"
    p[0] = p[1]

def p_idatrib_sigla(p):
    "idatrib : SIGLA"
    p[0] = p[1]

def p_idatrib_forma(p):
    "idatrib : FORMA"
    p[0] = p[1]

def p_idatrib_pais(p):
    "idatrib : PAIS"
    p[0] = p[1]

def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

parser = yacc.yacc()

with open('example.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    parser.success = True
    parser.flag = True
    parser.parse(content)