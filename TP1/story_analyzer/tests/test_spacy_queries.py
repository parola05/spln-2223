from unittest import TestCase
from story_analyzer.spacy_queries import SpacyQueries

class TestSpacyQueries(TestCase):
    def test_similar_sentence(self):
        queries = SpacyQueries("pt","O harry potter está com a Hermione a estudar. O Harry Potter está a jantar com o Ron.")
        self.assertEqual("O Harry Potter está a jantar com o Ron.", queries.similarSentence("O Harry está a comer.")[0])
