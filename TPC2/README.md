# TPC2

Criação de uma grámatica (e também o *parser* para gramática) orientada ao **conceito** (e não ao galego), tendo em conta os conceitos do ficheiro *medicina.pdf*

## Gramática orientada ao **conceito**

A linguagem orientada ao conceito num primeiro nível é caracterizada por uma lista de 

```
Dicionario -> Conceitos
Conceitos -> Conceitos SEPARADOR1 Conceito
           | vazio
Conceito -> Identidade_conceito SEPARADOR2 Areas SEPARADOR_CONCEITO_IN Linguas
Identidade_conceito -> INDEX
Areas -> Areas SEPARADOR_AREAS Area
Areas -> vazio
Area -> NOME
Linguas -> Linguas SEPARADOR3 Lingua
Linguas -> vazio
Lingua -> Identidade_lingua SEPARADOR4 Sinonimos
Identidade_lingua -> IDENTIDADE_LINGUA
Sinonimos -> Sinonimos SEPARADOR4 Sinonimo
Sinonimos -> vazio
Sinonimo -> NOME SEPARADOR5 Atributos
Atributos -> Atributos SEPARADOR5 Atributo
Atributos -> vazio
Atributo -> ID_Atrib SEPARADOR_ATRIBUTO NOME
ID_Atrib -> CATEGORIA
          | FORMA
          | PAIS
          | SIGLA 
```