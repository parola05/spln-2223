import newspaper
from newspaper import Article
import pickle
import sys 
import time

websiteUrl = sys.argv[1] if len(sys.argv)>=1 else ''
articlesDir = sys.argv[2] if len(sys.argv)>=2 else '.'

while True:
    time.sleep(86400) # sleep for a day before make new requests
    paper = newspaper.build(websiteUrl)
    for article in paper.articles:
        article = Article(article.url)
        article.download()
        article.parse()
        with open(articlesDir + "/" + article.url , "w") as file:
            pickle.dump(article, file)