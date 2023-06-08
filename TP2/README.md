# Shield 

1. [Contexto](#contexto)
2. [Caracterização do sistema](#caracterização-do-sistema)
   1. [Arquitetura](#arquitetura)
   2. [Anonimização de Nomes](#anonimização-de-nomes)
   3. [Anonimização de Endereços](#anonimização-de-endereços)
   4. [Anonimização de Documentos](#anonimização-de-documentos)
3. [Equipa](#equipa)

## Contexto

## Caracterização do sistema

### Arquitetura

 <img src="https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/arq.png" alt="Alex">

### Anonimização de Nomes


Os **nomes** anonimizados nesta etapa da ferramenta consistem em:

* **Nomes de Pessoas**: nomes próprios, apelidos, alcunhas. Por exemplo: *John Smith*, *Sarah*.
* **Nomes de Organizações**: nomes de entidades estruturadas, geralmente composta por um grupo de pessoas, que trabalha para atingir objetivos específicos. Por exemplo: *Acme Industries*, *World Wildlife Fund*.

Para a anonimização destes nomes foi decidido que, ao serem identificados, deviam ser substituídos pelas correspondentes iniciais intercaladas com o **ponto final**. A metodologia deste algoritmo baseou-se em três etapas:

1.  Detecção das entidades do texto.
2.  Filtragem das entidades que representam **pessoas** e **organizações**;
3. Substituição do nome destas entidades pelo seu nome anonimizado.

A etapa 1 e 2 foram concretizadas utilizando a biblioteca Spacy. Após carregar o modelo de processamento de texto no idioma do texto dado pelo utilizador e aplicar os processamentos linguísticos deste modelo no texto, é possível extrair as suas entidades da seguinte maneira:

```Python
nlp = spacy.load('en_core_web_sm')
doc = nlp(self.text)
for ent in doc.ents:
    if ent.label_ == "PERSON" or ent.label_ == "ORG":
        # substitution
```

Por outro lado, a etapa 3 foi realizada com técnicas de processamento de texto em Python, utilizando alguns métodos sobre *strings* e o módulo RE para expressões regulares. Dada uma entidade, os seus respectivos nomes foram separados a partir de um ou mais carácter de espaço em branco e, de seguida, o **nome anonimizado**  foi formado com as iniciais de cada nome concatenadas com o carácter **"."**. Uma vez em posse do nome anonimizado, bastava substituir todas as ocorrências do nome sem anonimização pelo termo anonimizado. 

```Python
if ent.label_ == "PERSON" or ent.label_ == "ORG":
    ent_names = re.split(r"\s+",ent.text)
    anonymized_name = ".".join(name[0] for name in ent_names)
    self.text = re.sub(ent.text,anonymized_name,self.text) 
```

É de se salientar que, inicialmente, foi utilizada a função *split* sobre *strings* com um único delimitador de ``espaço" para serem separados os nomes de uma entidade. Porém, esta alternativa não foi seguida, uma vez que alguns textos mal formados poderiam conter mais de um carácter de espaço em branco entre os nomes de uma entidade. Por isso que, como pode ser visto no código acima, foi utilizado o *split* do módulo RE que possibilitar a utilização de uma expressão regular para informar o delimitador do *split*.

### Anonimização de Endereços

### Anonimização de Documentos

## Autores

<h2>Autores</h2>

<div class="author-container">
  <div class="author">
    <img src="https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/henrique.jpeg
" alt="Henrique Parola">
    <p>Henrique Parola</p>
  </div>
  <div class="author">
    <img src="https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/jose.png" alt="José Pedro">
    <p>José Pedro</p>
  </div>
  <div class="author">
    <img src="https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/alex.png" alt="Alex">
    <p>Alex</p>
  </div>
</div>

<style>
.author-container {
  display: flex;
  width: 100%;
  height: 190px;
}

.author {
  flex: 1;
}
</style>

