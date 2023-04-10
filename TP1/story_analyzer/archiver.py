import shelve
from shelve import Shelf
import os
import copy
class Archiver:
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.path: str = os.path.join(self.home, ".story", "db", "archive")

    def addStory(self, title: str, bookObj : dict):
        print(os.path.dirname(self.path))
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        db: Shelf = shelve.open(self.path)
        if title in db.keys():
            copyDict : dict = copy.deepcopy(db[title])
            copyDict.update(bookObj)
            db[title] = copyDict
        else:
            db[title] = bookObj
        db.close()

    def getStory(self, title: str) -> dict:
        db: Shelf = shelve.open(self.path)
        bookObj = copy.deepcopy(db[title])
        db.close()
        return bookObj
