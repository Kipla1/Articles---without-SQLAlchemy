#!/usr/bin/env python3
"""
Database seed script to populate the database with test data
Should be placed in lib/db/seed.py
"""

import sqlite3
import sys
import os

# Add the lib directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from lib.db.connection import get_connection

def seed_database():
    """Populate database with test data"""
    conn = get_connection()
    c = conn.cursor()
    
    print("Seeding database with test data...")
    
    # Clear existing data (optional - for clean testing)
    c.execute("DELETE FROM articles")
    c.execute("DELETE FROM magazines") 
    c.execute("DELETE FROM authors")
    
    # Insert sample authors
    authors_data = [
        "John Smith",
        "Jane Doe", 
        "Bob Johnson",
        "Alice Williams",
        "Charlie Brown",
        "Diana Prince",
        "Frank Miller",
        "Grace Hopper"
    ]
    
    for author_name in authors_data:
        c.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
    
    # Insert sample magazines
    magazines_data = [
        ("Tech Today", "Technology"),
        ("Health Weekly", "Health"),
        ("Sports Digest", "Sports"),
        ("Science Now", "Science"),
        ("Art & Culture", "Arts"),
        ("Business World", "Business"),
        ("Travel Guide", "Travel"),
        ("Food & Wine", "Lifestyle")
    ]
    
    for name, category in magazines_data:
        c.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
    
    # Insert sample articles (ensuring some authors have multiple articles)
    articles_data = [
        ("The Future of AI", 1, 1),
        ("Machine Learning Basics", 1, 1),
        ("Neural Networks Explained", 1, 1),
        ("Healthy Eating Tips", 2, 2),
        ("Exercise for Beginners", 2, 2),
        ("Mental Health Matters", 2, 2),
        ("Football Season Preview", 3, 3),
        ("Basketball Analytics", 3, 3),
        ("Climate Change Research", 4, 4),
        ("Space Exploration", 4, 4),
        ("Quantum Computing", 4, 4),
        ("Modern Art Trends", 5, 5),
        ("Classical Music Revival", 5, 5),
        ("Startup Funding Guide", 6, 6),
        ("Investment Strategies", 6, 6),
        ("European Travel Tips", 7, 7),
        ("Asian Cuisine Guide", 8, 8),
        ("Wine Tasting Basics", 8, 8),
        ("Tech Industry Analysis", 1, 6),  # Cross-category article
        ("Sports Psychology", 2, 3),       # Cross-category article
        ("Art Therapy Benefits", 5, 2),    # Cross-category article
    ]
    
    for title, author_id, magazine_id in articles_data:
        c.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                 (title, author_id, magazine_id))
    
    conn.commit()
    conn.close()
    
    print("Database seeded successfully!")
    print(f"Added {len(authors_data)} authors")
    print(f"Added {len(magazines_data)} magazines") 
    print(f"Added {len(articles_data)} articles")

if __name__ == "__main__":
    seed_database()