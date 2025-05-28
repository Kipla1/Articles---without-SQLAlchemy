import sqlite3
from lib.db.connection import get_connection

def run_example_queries():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM authors;")
    authors = cursor.fetchall()
    print("Authors:")
    for author in authors:
        print(author)

    cursor.execute("SELECT * FROM articles;")
    articles = cursor.fetchall()
    print("\nArticles:")
    for article in articles:
        print(article)

    cursor.execute("SELECT * FROM magazines;")
    magazines = cursor.fetchall()
    print("\nMagazines:")
    for magazine in magazines:
        print(magazine)

    connection.close()

if __name__ == "__main__":
    run_example_queries()