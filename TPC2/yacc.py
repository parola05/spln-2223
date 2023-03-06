import sys
import ply.yacc as yacc
from lex import tokens

def p_dicionario(p):
    "dicionario : conceitos"

def p_conceitos(p):
    "conceitos : conceito SEPARADOR1 conceitos"

def p_conceitos_single(p):
    "conceitos : conceito"

def p_conceito(p):
    "conceito : identidadeconceito SEPARADOR2 AREAS SEPARADOR3 areas SEPARADOR2 LINGUAS SEPARADOR3 linguas"

def p_identidadeconceito(p):
    "identidadeconceito :  INDEX"

def p_areas(p):
    "areas : area SEPARADOR3 areas"

def p_areas_one(p):
    "areas : area"

def p_area(p):
    "area : NOME"

def p_linguas(p):
    "linguas : lingua SEPARADOR3 linguas"

def p_linguas_single(p):
    "linguas : lingua"

def p_lingua(p):
    "lingua : identidadelingua SEPARADOR4 sinonimos"

def p_identidadelingua(p):
    "identidadelingua : IDENTIDADELINGUA"

def p_sinonimos(p):
    "sinonimos : sinonimo SEPARADOR4 sinonimos"

def p_sinonimos_single(p):
    "sinonimos : sinonimo"

def p_sinonimo(p):
    "sinonimo : NOME SEPARADOR5 atributos"

def p_sinonimo_single(p):
    "sinonimo : NOME"

def p_atributos(p):
    "atributos : atributo SEPARADOR5 atributos"

def p_atributos_single(p):
    "atributos : atributo"

def p_atributo(p):
    "atributo : idatrib SEPARADOR6 NOME"

def p_idatrib_categoria(p):
    "idatrib : CATEGORIA"

def p_idatrib_sigla(p):
    "idatrib : SIGLA"

def p_idatrib_forma(p):
    "idatrib : FORMA"

def p_idatrib_pais(p):
    "idatrib : PAIS"

def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

parser = yacc.yacc()

with open('medicina_grammar.txt', 'r') as f:
    content = f.read()
    parser.success = True
    parser.flag = True
    parser.parse(content)