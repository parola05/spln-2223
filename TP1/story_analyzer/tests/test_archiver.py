from unittest import TestCase
from story_analyzer.archiver import Archiver

class TestArchiver(TestCase):
    def test_add_story(self):
        db = Archiver()
        harry = {"Harry Potter 1": {"title" : "Harry Potter 1", "text" : "You know who!"}}
        db.addStory("Harry Potter 1", harry)
        self.assertEqual(harry, db.getStory("Harry Potter 1"))
        self.assertNotEqual({}, db.getStory("Harry Potter 1"))
