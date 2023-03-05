# TPC2

Criação de uma grámatica (e também o *parser* para gramática) orientada ao **conceito** (e não ao galego), tendo em conta os conceitos do ficheiro *medicina.pdf*

## Gramática orientada ao **conceito**

```
Dicionario -> Conceitos
Conceitos -> Conceitos SEPARADOR1 Conceito
           | Conceito
Conceito -> Identidade_conceito SEPARADOR2 AREAS SEPARADOR3 Areas SEPARADOR2 LINGUAS SEPARADOR3 Linguas
Identidade_conceito -> INDEX
Areas -> Area SEPARADOR3 Areas
Areas -> Area
Area -> NOME
Linguas -> Lingua SEPARADOR3 Linguas
Linguas -> Lingua
Lingua -> Identidade_lingua SEPARADOR4 Sinonimos
Identidade_lingua -> IDENTIDADE_LINGUA
Sinonimos -> Sinonimo SEPARADOR4 Sinonimos
Sinonimos -> Sinonimo
Sinonimo -> NOME SEPARADOR5 Atributos
Sinonimo -> NOME
Atributos -> Atributo SEPARADOR5 Atributos
Atributos -> Atributo
Atributo -> ID_Atrib SEPARADOR6 NOME
ID_Atrib -> CATEGORIA
          | FORMA
          | PAIS
          | SIGLA 
```

Os **SEPARADORES** definidos servem para dar **identação** a sintaxe, sendo 
explicitamente definidos da seguinte forma:
* SEPARADOR6: **r'\n\ \ \ \ \ '**
* SEPARADOR5: **r'\n\ \ \ \ '**
* SEPARADOR4: **r'\n\ \ \ '**
* SEPARADOR3: **r'\n\ \ '**
* SEPARADOR2: **r'\n\ '**
* SEPARADOR1: **r'\n'**

## Estrutura de ficheiros

* **lex.py**: processador léxico
* **yacc.py**: processador sintático
* **lingua_oc\*.txt**: ficheiros de teste para a gramática desenvolvida 