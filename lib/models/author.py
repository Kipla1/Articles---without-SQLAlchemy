# from lib.db.connection import get_connection
import sqlite3


conn = sqlite3.connect('authors.db')
c = conn.c()
c.execute("""CREATE TABLE IF NOT EXISTS authors (
id INTEGER PRIMARY KEY,
name VARCHAR(255) NOT NULL
)""")
class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f"Author {self.name}"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    def save(self):
        """Save author to database"""
        if self.id is None:
            # Insert new author
            c.execute(
                "INSERT INTO authors (name) VALUES (?)",
                (self.name,)
            )
            self.id = c.lastrowid
        else:
            # Update existing author
            c.execute(
                "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
            )
        
        conn.commit()
        conn.close()
        return self
    
    @classmethod
    def find_by_id(cls, id):
        """Find author by ID"""
        c.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(name=row['name'], id=row['id'])
        return None
    
    @classmethod
    def find_by_name(cls, name):
        """Find author by name"""
        c.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(name=row['name'], id=row['id'])
        return None
    
    @classmethod
    def all(cls):
        """Get all authors"""
        c.execute("SELECT * FROM authors")
        rows = c.fetchall()
        conn.close()
        
        return [cls(name=row['name'], id=row['id']) for row in rows]
    
    def articles(self):
        """Get all articles written by this author"""
        c.execute("""
            SELECT * FROM articles
            WHERE author_id = ?
        """, (self.id,))
        rows = c.fetchall()
        conn.close()
        return rows
    
    def magazines(self):
        """Get all unique magazines this author has contributed to"""
        c.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = c.fetchall()
        conn.close()
        return rows
    
    def add_article(self, magazine, title):
        """Create and insert a new Article for this author"""
        from lib.models.article import Article
        
        if hasattr(magazine, 'id'):
            magazine_id = magazine.id
        else:
            magazine_id = magazine
        
        article = Article(title=title, author_id=self.id, magazine_id=magazine_id)
        return article.save()
    
    def topic_areas(self):
        """Get unique categories of magazines this author has contributed to"""
        c.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = c.fetchall()
        conn.close()
        return [row['category'] for row in rows]