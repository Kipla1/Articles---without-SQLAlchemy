import unittest
from lib.models.author import Author

class TestAuthor(unittest.TestCase):

    def setUp(self):
        self.author = Author(name="Test Author", email="test@example.com")

    def test_author_creation(self):
        self.assertEqual(self.author.name, "Test Author")
        self.assertEqual(self.author.email, "test@example.com")

    def test_author_sql_methods(self):
        # Assuming there are methods like save() and find() in Author class
        self.author.save()
        found_author = Author.find(self.author.id)
        self.assertEqual(found_author.name, self.author.name)
        self.assertEqual(found_author.email, self.author.email)

    def tearDown(self):
        # Clean up after tests, if necessary
        self.author.delete()  # Assuming a delete method exists

if __name__ == '__main__':
    unittest.main()