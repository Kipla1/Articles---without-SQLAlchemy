#!/usr/bin/env python3
"""
Interactive debugging script to test the models and database operations
"""

import sys
import os

# Add the lib directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def main():
    """Interactive debugging session"""
    print("=== Python App Debug Console ===")
    print("Available classes: Author, Magazine, Article")
    print("Type 'help()' for available methods or 'exit()' to quit")
    print()
    
    # Demo some functionality
    print("--- Sample Usage ---")
    
    # Get all authors
    print("All Authors:")
    authors = Author.all()
    for author in authors:
        print(f"  {author}")
    print()
    
    # Get all magazines
    print("All Magazines:")
    magazines = Magazine.all()
    for magazine in magazines:
        print(f"  {magazine}")
    print()
    
    # Get all articles
    print("All Articles:")
    articles = Article.all()
    for article in articles:
        print(f"  {article}")
    print()
    
    # Show author's articles and magazines
    for author in Author:
        author = authors[0]
        print(f"Articles by {author.name}:")
        author_articles = author.articles()
        for article in author_articles:
            print(f"  - {article.title}")
        
        print(f"Magazines {author.name} has written for:")
        author_magazines = author.magazines()
        for magazine in author_magazines:
            print(f"  - {magazine.name} ({magazine.category})")
        
        print(f"Topic areas for {author.name}: {author.topic_areas()}")
        print()
    
    # Show magazine's articles and contributors
    if magazines:
        magazine = magazines[0]
        print(f"Articles in {magazine.name}:")
        mag_articles = magazine.articles()
        for article in mag_articles:
            print(f"  - {article.title}")
        
        print(f"Contributors to {magazine.name}:")
        contributors = magazine.contributors()
        for contributor in contributors:
            print(f"  - {contributor.name}")
        print()
    
    # Find top publisher
    top_pub = Magazine.top_publisher()
    if top_pub:
        print(f"Top publisher: {top_pub.name}")
    
    print("\n--- Interactive Mode ---")
    print("You can now interact with the models directly.")
    print("Examples:")
    print("  author = Author.find_by_name('John Smith')")
    print("  magazine = Magazine.find_by_category('Technology')")
    print("  article = Article.find_by_title('The Future of AI')")
    print("  new_author = Author('New Author Name')")
    print("  new_author.save()")
    
    # Start interactive mode
    import code
    code.interact(local=locals())

def help():
    """Show available methods for each class"""
    print("\n=== Author Methods ===")
    print("Author(name, id=None)")
    print("  .save() - Save to database")
    print("  .articles() - Get author's articles")
    print("  .magazines() - Get magazines author has written for")
    print("  .add_article(magazine, title) - Add new article")
    print("  .topic_areas() - Get unique topic areas")
    print("  Author.find_by_id(id)")
    print("  Author.find_by_name(name)")
    print("  Author.all()")
    
    print("\n=== Magazine Methods ===")
    print("Magazine(name, category, id=None)")
    print("  .save() - Save to database")
    print("  .articles() - Get magazine's articles")
    print("  .contributors() - Get contributing authors")
    print("  .article_titles() - Get article titles")
    print("  Magazine.find_by_id(id)")
    print("  Magazine.find_by_name(name)")
    print("  Magazine.find_by_category(category)")
    print("  Magazine.all()")
    print("  Magazine.top_publisher()")
    
    print("\n=== Article Methods ===")
    print("Article(title, author_id, magazine_id, id=None)")
    print("  .save() - Save to database")
    print("  .author() - Get article's author")
    print("  .magazine() - Get article's magazine")
    print("  Article.find_by_id(id)")
    print("  Article.find_by_title(title)")
    print("  Article.all()")

if __name__ == "__main__":
    main()