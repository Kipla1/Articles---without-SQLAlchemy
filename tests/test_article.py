import unittest
from lib.models.article import Article

class TestArticle(unittest.TestCase):

    def setUp(self):
        self.article = Article(title="Sample Article", content="This is a sample article.")

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Sample Article")
        self.assertEqual(self.article.content, "This is a sample article.")

    def test_article_methods(self):
        # Assuming there are methods like save and delete in the Article class
        self.article.save()
        self.assertIsNotNone(self.article.id)  # Check if the article has an ID after saving

        self.article.delete()
        self.assertIsNone(self.article.id)  # Check if the article is deleted

if __name__ == '__main__':
    unittest.main()