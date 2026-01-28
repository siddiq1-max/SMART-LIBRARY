from app import create_app, db
from app.models import Book, User
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

app = create_app()

def seed_data():
    with app.app_context():
        print("Seeding data...")
        
        # 1. Create Books
        categories = ['Fiction', 'Science Fiction', 'Business', 'Technology', 'Biography', 'History', 'Comics']
        
        sample_books = [
            {
                'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'category': 'Fiction',
                'isbn': '9780743273565', 'price': 10.99, 'pages': 180, 'rating': 4.5,
                'cover': 'https://covers.openlibrary.org/b/id/12555314-L.jpg' 
            },
            {
                'title': 'Dune', 'author': 'Frank Herbert', 'category': 'Science Fiction',
                'isbn': '9780441013593', 'price': 18.99, 'pages': 412, 'rating': 4.8,
                'cover': 'https://covers.openlibrary.org/b/id/12696078-L.jpg'
            },
            {
                'title': 'Zero to One', 'author': 'Peter Thiel', 'category': 'Business',
                'isbn': '9780804139298', 'price': 14.50, 'pages': 210, 'rating': 4.6,
                'cover': 'https://covers.openlibrary.org/b/id/8376510-L.jpg'
            },
            {
                'title': 'Clean Code', 'author': 'Robert C. Martin', 'category': 'Technology',
                'isbn': '9780132350884', 'price': 35.00, 'pages': 464, 'rating': 4.9,
                'cover': 'https://covers.openlibrary.org/b/id/12539690-L.jpg'
            },
            {
                'title': 'Steve Jobs', 'author': 'Walter Isaacson', 'category': 'Biography',
                'isbn': '9781451648539', 'price': 20.00, 'pages': 656, 'rating': 4.7,
                'cover': 'https://covers.openlibrary.org/b/id/7356399-L.jpg'
            },
            {
                'title': 'Sapiens', 'author': 'Yuval Noah Harari', 'category': 'History',
                'isbn': '9780062316097', 'price': 16.99, 'pages': 443, 'rating': 4.8,
                'cover': 'https://covers.openlibrary.org/b/id/8259443-L.jpg'
            },
            {
                'title': 'Watchmen', 'author': 'Alan Moore', 'category': 'Comics',
                'isbn': '9780930289232', 'price': 19.99, 'pages': 416, 'rating': 4.9,
                'cover': 'https://covers.openlibrary.org/b/id/10582294-L.jpg'
            },
             {
                'title': '1984', 'author': 'George Orwell', 'category': 'Fiction',
                'isbn': '9780451524935', 'price': 9.99, 'pages': 328, 'rating': 4.6,
                'cover': 'https://covers.openlibrary.org/b/id/12556556-L.jpg'
            },
             {
                'title': 'The Pragmatic Programmer', 'author': 'Andrew Hunt', 'category': 'Technology',
                'isbn': '9780201616224', 'price': 32.95, 'pages': 352, 'rating': 4.8,
                'cover': 'https://covers.openlibrary.org/b/id/12696085-L.jpg'
            },
             {
                'title': 'Atomic Habits', 'author': 'James Clear', 'category': 'Business',
                'isbn': '9780735211292', 'price': 15.00, 'pages': 320, 'rating': 4.9,
                'cover': 'https://covers.openlibrary.org/b/id/8525044-L.jpg'
            }
        ]

        for b_data in sample_books:
            # Construct reliable Cover URL using ISBN
            isbn_cover = f"https://covers.openlibrary.org/b/isbn/{b_data['isbn']}-L.jpg"
            
            # Check if exists
            existing_book = Book.query.filter_by(isbn=b_data['isbn']).first()
            
            if existing_book:
                print(f"Updating {b_data['title']}...")
                existing_book.cover_image = isbn_cover
                existing_book.price = b_data['price'] # Ensure price is set
                existing_book.pages = b_data['pages']
                existing_book.average_rating = b_data['rating']
            else:
                print(f"Adding {b_data['title']}...")
                book = Book(
                    title=b_data['title'],
                    author=b_data['author'],
                    isbn=b_data['isbn'],
                    category=b_data['category'],
                    cover_image=isbn_cover,
                    price=b_data['price'],
                    pages=b_data['pages'],
                    average_rating=b_data['rating'],
                    rating_count=random.randint(10, 500),
                    quantity=random.randint(1, 10),
                    available_count=random.randint(1, 10),
                    description=f"A fantastic book about {b_data['category']}. Must read!",
                    language='English',
                    publication_year=random.randint(1990, 2023)
                )
                db.session.add(book)
        
        db.session.commit()
        print("Database seeded and updated successfully!")

if __name__ == '__main__':
    seed_data()
