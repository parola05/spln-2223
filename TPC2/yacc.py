import sys
import ply.yacc as yacc
from lex import tokens

def p_dicionario(p):
    "dicionario : conceitos"
    #print("Detetado dicionario")

def p_conceitos(p):
    "conceitos : conceito SEPARADOR1 conceitos"
    #print("Detetado conceitos: ", p[0])

def p_conceitos_single(p):
    "conceitos : conceito"
    #print("Detetado conceitos: ", p[0])

def p_conceito(p):
    "conceito : identidadeconceito SEPARADOR2 AREAS SEPARADOR3 areas SEPARADOR2 LINGUAS SEPARADOR3 linguas"
    #print("Detetado conceito")

def p_identidadeconceito(p):
    "identidadeconceito :  INDEX"
    print("Detetado identidadeconceito: ", p[1])

def p_areas(p):
    "areas : area SEPARADOR3 areas"
    #print("Detetado areas")

def p_areas_one(p):
    "areas : area"
    #print("Detetado area final")

def p_area(p):
    "area : NOME"
    print("Detetado area: ", p[1])

def p_linguas(p):
    "linguas : lingua SEPARADOR3 linguas"
    #print("Detetado linguas")

def p_linguas_single(p):
    "linguas : lingua"
    #print("Detetado linguas single")

def p_lingua(p):
    "lingua : identidadelingua SEPARADOR4 sinonimos"
    #print("Detetado lingua")

def p_identidadelingua(p):
    "identidadelingua : IDENTIDADELINGUA"
    print("Detetado identidade da lingua: ", p[1])

def p_sinonimos(p):
    "sinonimos : sinonimo SEPARADOR4 sinonimos"
    #print("Detetado sinonimos")

def p_sinonimos_single(p):
    "sinonimos : sinonimo"
    #print("Detetado sinonimos single")

def p_sinonimo(p):
    "sinonimo : NOME SEPARADOR5 atributos"
    print("Detetado sinonimo", p[1])

def p_sinonimo_single(p):
    "sinonimo : NOME"
    print("Detetado sinonimo sem atributos", p[1])

def p_atributos(p):
    "atributos : atributo SEPARADOR5 atributos"
    #print("Detetado atributos")

def p_atributos_single(p):
    "atributos : atributo"
    #print("Detetado atributos single")

def p_atributo(p):
    "atributo : idatrib SEPARADOR6 NOME"
    print("Detetado atributo", p[3])

def p_idatrib_categoria(p):
    "idatrib : CATEGORIA"
    print("Detetado idatrib", p[1])

def p_idatrib_sigla(p):
    "idatrib : SIGLA"
    print("Detetado idatrib", p[1])

def p_idatrib_forma(p):
    "idatrib : FORMA"
    print("Detetado idatrib", p[1])

def p_idatrib_pais(p):
    "idatrib : PAIS"
    print("Detetado idatrib", p[1])

def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

parser = yacc.yacc()

with open('lingua_oc.txt', 'r') as f:
    content = f.read()
    parser.success = True
    parser.flag = True
    parser.parse(content)