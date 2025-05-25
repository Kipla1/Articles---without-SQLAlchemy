from lib.db.connection import get_connection


c = get_connection.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS authors(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
    )""")

class Author:
    pass

get_connection.commit()
get_connection.close()