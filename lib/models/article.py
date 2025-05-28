from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
    
    def __repr__(self):
        return f"Article({self.title})"
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        self._title = value
    
    def save(self):
        """Save article to database"""
        conn = get_connection()
        c = conn.cursor()
        
        if self.id is None:
            c.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = c.lastrowid
        else:
            c.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        
        conn.commit()
        conn.close()
        return self
    
    @classmethod
    def find_by_id(cls, id):
        """Find article by ID"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(title=row['title'], author_id=row['author_id'], 
                      magazine_id=row['magazine_id'], id=row['id'])
        return None
    
    @classmethod
    def find_by_title(cls, title):
        """Find article by title"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(title=row['title'], author_id=row['author_id'], 
                      magazine_id=row['magazine_id'], id=row['id'])
        return None
    
    @classmethod
    def all(cls):
        """Get all articles"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM articles")
        rows = c.fetchall()
        conn.close()
        
        return [cls(title=row['title'], author_id=row['author_id'], 
                   magazine_id=row['magazine_id'], id=row['id']) for row in rows]
    
    def author(self):
        """Get the author of this article"""
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)
    
    def magazine(self):
        """Get the magazine this article was published in"""
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)