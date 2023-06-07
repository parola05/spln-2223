# **Web Scrapping** periódico de jornais

<img src="./images/banner.png" width=100%>

## Descrição

Criação de um serviço de **armazenamento de artigos** de um *website*. Periodicamente (a cada 24 horas) são recolhidos os artigos do *website* indicado e salvos numa diretória destinada a estes artigos.

## Método

Através do **url** indicado pelo utilizador é realizado o método *build* da biblioteva *newspaper*. Tal método retorna a *url* dos artigos existentes neste *website*. A partir destas *urls* são criados os objetos *Article* (também da biblioteca *newspaper*) e feito o *download* e *parse* de cada artigo. 

Uma vez feitas estas operações é então realizado o salvamento destes objetos na diretoria indicada. Para este efeito é utilizado o módulo *pickle* para a serialização destes objetos durante o processo de salvamento.

Um detalhe importante é que o programa se encontra em ciclo infinito, realizando os *requests* dos artigos a cada 24 horas.

## Ficheiros

* *np.py*: programa desenvolvido. Modos de uso:
    * *primeiro parâmetro*: **url** do *website* para recolha dos artigos
    * *segundo parâmetro*: diretório para armazenamento dos artigos

## Dependências

* newspaper3k