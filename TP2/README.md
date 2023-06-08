<h1 style="font-size:60px" align="center"><img height=58cm src="https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/logo.png"> HShield</h1>

<h4 align="center">A ferramenta ideal para anonimização de dados pessoais dos seus documentos</h4>

<br>

<img src="https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/banner.png">

<br>

1. [🌟 Introdução](#introducao)
   1. [Contexto](#contexto)
   2. [Propósito e Objetivos](#proposito-e-objetivos)
2. [⚙️ Caracterização do sistema](#caracterização-do-sistema)
   1. [Arquitetura](#arquitetura)
   2. [Anonimização de Nomes](#anonimização-de-nomes)
   3. [Anonimização de Endereços](#anonimização-de-endereços)
   4. [Anonimização de Documentos](#anonimização-de-documentos)
3. [👥 Equipa](#equipa)

## 🌟 Introdução

### Contexto

A privacidade de um indivíduo está intimamente ligada aos seus dados. Dados os quais, nos dias de hoje, são gerados numa quantidade nunca antes vista através da Internet. Estas dados, quando não são cuidadosamente tratados, podem afetar a segurança das pessoas. Neste segmento que surge o conceito de anonimização dos dados.

Uma definição conceptual da anonimização de dados pode ser ["para anonimizar quaisquer dados, têm de lhes ser retirados elementos suficientes para que deixe de ser possível identificar (de forma irreversível) o titular dos dados"](https://www.uc.pt/protecao-de-dados/protecao-de-dados-pessoais/anonimizacao-e-pseudonimizacao/) 
. Neste contexto surge o Regulamento Geral de Proteção de Dados (RGPD), como tabmém a A Lei Geral de Proteção de Dados Pessoais (LGPD) que define um [dado anonimizado  aquele que, originariamente, era relativo a uma pessoa, mas que passou por etapas que garantiram a desvinculação dele a essa pessoa](https://www.serpro.gov.br/lgpd/menu/protecao-de-dados/dados-anonimizados-lgpd). Conforme a LGPD, [alguns exemplos de dados pessoais são: nome, CPF, e-mail, idade, profissão, foto, entre outros](https://blog.hosts.green/dados-anonimizados/).

### Propósito e Objetivos

O propósito deste projeto é garantir a anonimização dos dados sensíveis pessoais presentes em documentos. Assim, o seu objetivo é concretizar um *software* que realiza uma série de tratamento de dados por forma a desvincular os dados das pessoas identificadas por eles. Este tratamento de dados resultará numa conversão de um dado documento numa versão sua anonimizada. Dentre as diversas formas de dados pessoais existentes, foram consideradas: o nome das pessoas/organizações, endereços (físicos ou na Web) e números identificadores de documentos (como o CC, carta de condução, entre outros).

Em suma, o objetivo principal do sistema é garantir a segurança dos indíviduos através de processos de anonimização. Uma vez que existem diversas formas de se concretizar esta tarefa, [não havendo um processo único de anonimização, a solução ideal será a que apresente em cada processo a maior impossibilidade da “re-identificação dos titulares dos dados”. Por princípio, a anonimização deverá ser um processo irreversível, análogo à destruição.](https://www.uc.pt/protecao-de-dados/protecao-de-dados-pessoais/anonimizacao-e-pseudonimizacao/)


## ⚙️ Caracterização do sistema

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

## 👥 Equipa

| ![Henrique Parola](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/henrique.jpeg) | ![José Pedro](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/jose.png) | ![Alex](https://raw.githubusercontent.com/LittleLevi05/spln-2223/main/TP2/images/alex.png) |
|:---:|:---:|:---:|
| Henrique Parola | José Pedro | Alex |