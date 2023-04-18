import newspaper
import time

urls = [
    'https://jornaldeangola.sapo.ao/',
    'https://www.novojornal.co.ao/',
    'https://www.opais.net/'
]


articles = []

for url in urls:
    time.sleep(5)
    paper = newspaper.build(url)
    for article in paper.articles:
        try:
            article.download()
            article.parse()
            articles.append(article)
        except:
            continue