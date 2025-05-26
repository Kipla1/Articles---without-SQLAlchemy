import sqlite3

conn = sqlite3.connect('magazines.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS magazines (
id INTEGER PRIMARY KEY,
name VARCHAR(255) NOT NULL,
category VARCHAR(255) NOT NULL
)""")
