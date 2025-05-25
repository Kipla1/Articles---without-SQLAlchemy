import sqlite3
import os

def setup_database(db_path):
    """Create a new database and set up the schema."""
    if os.path.exists(db_path):
        os.remove(db_path)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Read the SQL schema from the schema.sql file
    with open(os.path.join(os.path.dirname(__file__), '../lib/db/schema.sql'), 'r') as f:
        schema = f.read()

    # Execute the schema to create tables
    cursor.executescript(schema)

    connection.commit()
    connection.close()

def seed_database(db_path):
    """Seed the database with initial data."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Read the seed data from the seed.py file
    from lib.db.seed import seed_data
    seed_data(cursor)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    database_path = 'my_database.db'  # Specify your database file name
    setup_database(database_path)
    seed_database(database_path)
    print("Database setup and seeded successfully.")