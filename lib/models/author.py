from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f"Author({self.name})"
    
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
        conn = get_connection()
        c = conn.cursor()
        
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
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(name=row['name'], id=row['id'])
        return None
    
    @classmethod
    def find_by_name(cls, name):
        """Find author by name"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(name=row['name'], id=row['id'])
        return None
    
    @classmethod
    def all(cls):
        """Get all authors"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM authors")
        rows = c.fetchall()
        conn.close()
        
        return [cls(name=row['name'], id=row['id']) for row in rows]
    
    def articles(self):
        """Get all articles written by this author"""
        from lib.models.article import Article
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT * FROM articles
            WHERE author_id = ?
        """, (self.id,))
        rows = c.fetchall()
        conn.close()
        return [Article(title=row['title'], author_id=row['author_id'], 
                       magazine_id=row['magazine_id'], id=row['id']) for row in rows]
    
    def magazines(self):
        """Get all unique magazines this author has contributed to"""
        from lib.models.magazine import Magazine
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = c.fetchall()
        conn.close()
        return [Magazine(name=row['name'], category=row['category'], id=row['id']) for row in rows]
    
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
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = c.fetchall()
        conn.close()
        return [row['category'] for row in rows]