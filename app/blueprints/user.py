from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Book, Transaction, Reservation
from app import db
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    # Current Loans
    current_loans = Transaction.query.filter_by(user_id=current_user.id, status='issued').all()
    # Reservations
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    # History (Returned)
    history_count = Transaction.query.filter_by(user_id=current_user.id, status='returned').count()
    
    return render_template('user/dashboard.html', 
                           current_loans=current_loans, 
                           reservations=reservations,
                           history_count=history_count)

@user_bp.route('/books')
@login_required
def search_books():
    query = request.args.get('q', '')
    category_filter = request.args.get('category', '')
    
    if query or category_filter:
        # If searching, show standard grid results
        books_query = Book.query
        if query:
            books_query = books_query.filter(Book.title.contains(query) | Book.author.contains(query))
        if category_filter:
            books_query = books_query.filter(Book.category == category_filter)
        results = books_query.all()
        return render_template('user/search.html', results=results, is_search=True, categories=[])
    else:
        # Default view: Group by Category (BookMyShow style)
        categories = [r[0] for r in db.session.query(Book.category).distinct().all()]
        ordered_books = {}
        for cat in categories:
            # Fetch up to 10 books per category for the carousel
            books = Book.query.filter_by(category=cat).limit(10).all()
            if books:
                ordered_books[cat] = books
        
        return render_template('user/search.html', ordered_books=ordered_books, is_search=False, categories=categories)

@user_bp.route('/book/<int:book_id>')
@login_required
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    # Similar Books (Same Category, exclude current)
    similar_books = Book.query.filter(Book.category == book.category, Book.id != book.id).limit(6).all()
    if not similar_books:
        # Fallback to random if no similar
        similar_books = Book.query.filter(Book.id != book.id).limit(6).all()
        
    return render_template('user/book_details.html', book=book, similar_books=similar_books)

@user_bp.route('/book/<int:book_id>/reserve', methods=['POST'])
@login_required
def reserve_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_count < 1:
        # Check if already reserved
        existing_res = Reservation.query.filter_by(user_id=current_user.id, book_id=book.id, status='pending').first()
        if existing_res:
            flash('You have already reserved this book.', 'warning')
        else:
            res = Reservation(user_id=current_user.id, book_id=book.id)
            db.session.add(res)
            db.session.commit()
            flash('Reservation placed successfully! You will be notified when available.', 'success')
    else:
        # If available, user can technically reserve it for pickup
        res = Reservation(user_id=current_user.id, book_id=book.id, status='approved') # Approved immediately for pickup
        db.session.add(res)
        db.session.commit()
        flash('Book reserved for pickup!', 'success')
        
@user_bp.route('/book/<int:book_id>/buy', methods=['POST'])
@login_required
def buy_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.quantity > 0:
        # Create Sales Transaction
        sale = Transaction(
            user_id=current_user.id,
            book_id=book.id,
            transaction_type='purchase',
            amount=book.price,
            status='completed',
            due_date=None, # No due date for sales
            return_date=datetime.utcnow() # Sold date
        )
        
        # Decrement stock
        book.quantity -= 1
        book.available_count -= 1
        
        # Credit Seller Wallet if applicable
        if book.seller_id:
            seller = book.seller
            seller.wallet_balance += book.price
        
        db.session.add(sale)
        db.session.commit()
        flash(f'Successfully purchased "{book.title}" for ${book.price}!', 'success')
    else:
        flash('Sorry, this book is out of stock.', 'danger')
        
    return redirect(url_for('user.book_details', book_id=book.id))

@user_bp.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        description = request.form.get('description')
        
        # Simple placeholder cover for user uploads or use ISBN
        cover_image = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg" if isbn else None
        
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            price=price,
            description=description,
            cover_image=cover_image,
            seller_id=current_user.id,
            total_quantity=1, # Users sell 1 copy usually
            quantity=1,
            available_count=1,
            pages=100, # Default
            average_rating=0
        )
        db.session.add(book)
        db.session.commit()
        flash('Book listed for sale successfully!', 'success')
        return redirect(url_for('user.my_listings'))
        
    return render_template('user/sell_book.html')

@user_bp.route('/my-listings')
@login_required
def my_listings():
    listings = Book.query.filter_by(seller_id=current_user.id).all()
    return render_template('user/my_listings.html', listings=listings)
