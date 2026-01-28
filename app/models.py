from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user') # admin, librarian, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile fields
    full_name = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    wallet_balance = db.Column(db.Float, default=0.0)

    # Relationships
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    books_for_sale = db.relationship('Book', backref='seller', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True, nullable=False)
    author = db.Column(db.String(100), index=True, nullable=False)
    isbn = db.Column(db.String(20), unique=True, index=True)
    category = db.Column(db.String(50), index=True)
    language = db.Column(db.String(30))
    publication_year = db.Column(db.Integer)
    publisher = db.Column(db.String(100))
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200)) # Path to image
    quantity = db.Column(db.Integer, default=1)
    available_count = db.Column(db.Integer, default=1)
    
    # New Fields for BookMyShow style
    price = db.Column(db.Float, default=0.0) # Purchasing price or Borrow fee
    pages = db.Column(db.Integer)
    average_rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    
    # User Seller Field
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Null if library owned
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='book', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='book', lazy='dynamic')
    reviews = db.relationship('Review', backref='book', lazy='dynamic')

    def __repr__(self):
        return f'<Book {self.title}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True) # Nullable for purchases
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='issued') # issued, returned, overdue, lost, completed (for sales)
    fine_amount = db.Column(db.Float, default=0.0)
    
    # New Fields for Sales
    transaction_type = db.Column(db.String(20), default='borrow') # borrow, purchase
    amount = db.Column(db.Float, default=0.0) # Cost of purchase

    def __repr__(self):
        return f'<Transaction {self.id} - {self.status}>'

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, approved, cancelled, fulfilled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reservation {self.id}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer) # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
