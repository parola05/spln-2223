import shelve
from shelve import Shelf
import os
class Archiver:
    def __init__(self):
        self.path: str = os.path.dirname(__file__) + "/db/archive"
        self.db: Shelf = shelve.open(self.path)

    def addStory(self, title: str, storyObj : dict):
        self.db[title] = storyObj

    def getStory(self, title: str) -> dict:
        return self.db.get(title)
