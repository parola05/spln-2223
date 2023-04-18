import newspaper
import time
import pickle

urls = [
    'https://jornaldeangola.sapo.ao/',
    'https://www.novojornal.co.ao/',
    'https://www.opais.net/'
]

articles = []
i = 0

for url in urls:
    time.sleep(5)
    print("Build do newspaper " + url + " ...")
    paper = newspaper.build(url)
    for article in paper.articles:
        try:
            print("Download do artigo " + i + " ...")
            article.download()
            article.parse()
            with open("articles\\" + url + "\\" + i, "wb") as file:
                pickle.dump(article, file)
            i = i + 1
        except:
            continue