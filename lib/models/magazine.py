import sqlite3
# from unicodedata import category

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Invalid name. Try again")
        else:
            self._name = value
            
    def save_magazine(self):
        conn = sqlite3.connect('magazines.db')
        c = conn.cursor()
        if self.id is None:
                c.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
                self.id = c.lastrowid
        else:
                c.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
        conn.commit()
        conn.close()
    
    @classmethod
    def findByName(cls, name):
        conn = sqlite3.connect('magazines.db')
        c = conn.cursor()
        c.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        magazine = c.fetchone()
        conn.close()
        return magazine
    
    @classmethod
    def findById(cls, id):
        conn = sqlite3.connect('magazines.db')
        c = conn.cursor()
        c.execute("SELECT * FROM magazines WHERE id = ?", (id))
        magazine = c.fetchone()
        conn.close()
        return magazine
    
    @classmethod
    def findByCategory(cls, category):
        conn = sqlite3.connect('magazines.db')
        c = conn.cursor()
        c.execute("SELECt * FROM magazines WHERE category = ?", (category))
        magazine = c.fetchone()
        conn.close()
        return magazine
    
    @classmethod
    def all_magazines(cls):
        conn = sqlite3.connect('magazines.db')
        c = conn.cursor()
        c.execute("SELECT * FROM magazines")
        all = c.fetchall()
        conn.close()
        return [cls(name=row['name'], category = row['category'], id = row['id'] )for row in all]    

    def articles(self):
        conn =sqlite3.connect()
# magazine2 = Magazine("samaritan", "healthy")
# magazine2.save_magazine()

found_magazine = Magazine.find_magazine("samaritan")
print(found_magazine)

