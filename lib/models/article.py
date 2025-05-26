import sqlite3

conn = sqlite3.connect('articles.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS articles (
id INTEGER PRIMARY KEY,
title VARCHAR(255) NOT NULL,
author_id INTEGER,
magazine_id INTEGER,
FOREIGN KEY (author_id) REFERENCES authors(id),
FOREIGN KEY (magazine_id) REFERENCES magazines(id)
)""")