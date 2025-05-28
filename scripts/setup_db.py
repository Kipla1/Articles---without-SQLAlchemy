#!/usr/bin/env python3
"""
Database setup script to create tables and populate with sample data
"""

import sqlite3
import os

def setup_database():
    """Create database tables and populate with sample data"""
    
    # Remove existing database file if it exists
    if os.path.exists('articles.db'):
        os.remove('articles.db')
    
    # Create connection
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    print("Creating database tables...")
    
    # Create tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )
    """)
    
    print("Populating with sample data...")
    
    # Insert sample authors
    authors = [
        "John Smith",
        "Jane Doe", 
        "Bob Johnson",
        "Alice Williams",
        "Charlie Brown"
    ]
    
    for author in authors:
        c.execute("INSERT INTO authors (name) VALUES (?)", (author,))
    
    # Insert sample magazines
    magazines = [
        ("Tech Today", "Technology"),
        ("Health Weekly", "Health"),
        ("Sports Digest", "Sports"),
        ("Science Now", "Science"),
        ("Art & Culture", "Arts")
    ]
    
    for name, category in magazines:
        c.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
    
    # Insert sample articles
    articles = [
        ("The Future of AI", 1, 1),
        ("Machine Learning Basics", 2, 1),
        ("Healthy Eating Tips", 3, 2),
        ("Exercise for Beginners", 1, 2),
        ("Football Season Preview", 4, 3),
        ("Basketball Analytics", 2, 3),
        ("Climate Change Research", 5, 4),
        ("Space Exploration", 3, 4),
        ("Modern Art Trends", 4, 5),
        ("Classical Music Revival", 5, 5)
    ]
    
    for title, author_id, magazine_id in articles:
        c.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                 (title, author_id, magazine_id))
    
    conn.commit()
    conn.close()
    
    print("Database setup complete!")
    print("Created 'articles.db' with sample data")

if __name__ == "__main__":
    setup_database()