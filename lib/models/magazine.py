from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category
    
    def __repr__(self):
        return f"Magazine({self.name}, {self.category})"
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value
            
    def save(self):
        """Save magazine to database"""
        conn = get_connection()
        c = conn.cursor()
        
        if self.id is None:
            c.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", 
                     (self.name, self.category))
            self.id = c.lastrowid
        else:
            c.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", 
                     (self.name, self.category, self.id))
        
        conn.commit()
        conn.close()
        return self
    
    @classmethod
    def find_by_name(cls, name):
        """Find magazine by name"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(name=row['name'], category=row['category'], id=row['id'])
        return None
    
    @classmethod
    def find_by_id(cls, id):
        """Find magazine by ID"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(name=row['name'], category=row['category'], id=row['id'])
        return None
    
    @classmethod
    def find_by_category(cls, category):
        """Find magazines by category"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = c.fetchall()
        conn.close()
        
        return [cls(name=row['name'], category=row['category'], id=row['id']) for row in rows]
    
    @classmethod
    def all(cls):
        """Get all magazines"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM magazines")
        rows = c.fetchall()
        conn.close()
        
        return [cls(name=row['name'], category=row['category'], id=row['id']) for row in rows]    

    def articles(self):
        """Get all articles published in this magazine"""
        from lib.models.article import Article
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = c.fetchall()
        conn.close()
        
        return [Article(title=row['title'], author_id=row['author_id'], 
                       magazine_id=row['magazine_id'], id=row['id']) for row in rows]
    
    def contributors(self):
        """Get all authors who have written for this magazine"""
        from lib.models.author import Author
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = c.fetchall()
        conn.close()
        
        return [Author(name=row['name'], id=row['id']) for row in rows]
    
    def article_titles(self):
        """Get all article titles published in this magazine"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = c.fetchall()
        conn.close()
        
        return [row['title'] for row in rows]
    
    def contributing_authors(self):
        """Get all authors who have written for this magazine (same as contributors)"""
        return self.contributors()
    
    @classmethod
    def top_publisher(cls):
        """Find the magazine with the most articles"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT m.*, COUNT(a.id) as article_count 
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = c.fetchone()
        conn.close()
        
        if row:
            return cls(name=row['name'], category=row['category'], id=row['id'])
        return None