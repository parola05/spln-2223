import ply.lex as lex

tokens = ( 'CATEGORIA', 'FORMA', 'PAIS', 'SIGLA', 'INDEX', 'NOME', 'IDENTIDADELINGUA', 'SEPARADOR1', 'SEPARADOR2', 'SEPARADOR3', 'SEPARADOR4', 'SEPARADOR5', 'SEPARADOR6','AREAS', 'LINGUAS')
 
def t_CATEGORIA(t):
    r'Categoria'
    return t

def t_FORMA(t):
    r'Forma'
    return t

def t_PAIS(t):
    r'Pais'
    return t

def t_SIGLA(t):
    r'Sigla'
    return t

def t_AREAS(t):
    r'Areas'
    return t

def t_LINGUAS(t):
    r'Linguas'
    return t

def t_IDENTIDADELINGUA(t):
    r'"es"|"pt"|"la"|"en"|"ga"'
    return t

def t_SEPARADORATRIBUTO(t):
    r'='
    return t

def t_INDEX(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_NOME(t):
    r'\w+(\ \w+)*'
    return t

def t_SEPARADOR6(t):
    r'\n\ \ \ \ \ '
    t.lexer.lineno += len(t.value)
    return t

def t_SEPARADOR5(t):
    r'\n\ \ \ \ '
    t.lexer.lineno += len(t.value)
    return t

def t_SEPARADOR4(t):
    r'\n\ \ \ '
    t.lexer.lineno += len(t.value)
    return t

def t_SEPARADOR3(t):
    r'\n\ \ '
    t.lexer.lineno += len(t.value)
    return t

def t_SEPARADOR2(t):
    r'\n\ '
    t.lexer.lineno += len(t.value)
    return t

def t_SEPARADOR1(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = '\t'
 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()