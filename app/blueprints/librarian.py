from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.decorators import librarian_required
from app.models import Book, Transaction, Reservation, User
from app.forms import BookForm
from app import db
from datetime import datetime, timedelta

librarian_bp = Blueprint('librarian', __name__)

@librarian_bp.route('/dashboard')
@login_required
@librarian_required
def dashboard():
    books_count = Book.query.count()
    low_stock = Book.query.filter(Book.available_count < 2).count()
    pending_reservations = Reservation.query.filter_by(status='pending').count() + Reservation.query.filter_by(status='approved').count()
    return render_template('librarian/dashboard.html', books_count=books_count, low_stock=low_stock, pending_reservations=pending_reservations)

@librarian_bp.route('/books')
@login_required
@librarian_required
def manage_books():
    books = Book.query.all()
    return render_template('librarian/manage_books.html', books=books)

@librarian_bp.route('/books/add', methods=['GET', 'POST'])
@login_required
@librarian_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            category=form.category.data,
            quantity=int(form.quantity.data),
            available_count=int(form.quantity.data),
            description=form.description.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('librarian.manage_books'))
    return render_template('librarian/add_book.html', form=form, title="Add Book")

@librarian_bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
@librarian_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.category = form.category.data
        diff = int(form.quantity.data) - book.quantity
        book.quantity = int(form.quantity.data)
        book.available_count += diff
        book.description = form.description.data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('librarian.manage_books'))
    return render_template('librarian/add_book.html', form=form, title="Edit Book")

@librarian_bp.route('/books/delete/<int:book_id>')
@login_required
@librarian_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted.', 'success')
    return redirect(url_for('librarian.manage_books'))

# --- Transaction Management ---

@librarian_bp.route('/reservations')
@login_required
@librarian_required
def manage_reservations():
    reservations = Reservation.query.filter(Reservation.status.in_(['pending', 'approved'])).all()
    return render_template('librarian/reservations.html', reservations=reservations)

@librarian_bp.route('/issue/<int:reservation_id>')
@login_required
@librarian_required
def issue_book(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    book = reservation.book
    
    if book.available_count < 1:
        flash('Cannot issue book. Out of stock.', 'danger')
        return redirect(url_for('librarian.manage_reservations'))
        
    # Create Transaction
    # Rule: 14 days loan period
    due_date = datetime.utcnow() + timedelta(days=14)
    transaction = Transaction(
        user_id=reservation.user_id,
        book_id=reservation.book_id,
        due_date=due_date,
        status='issued'
    )
    
    # Update Book stock
    book.available_count -= 1
    
    # Update Reservation
    reservation.status = 'fulfilled'
    
    db.session.add(transaction)
    db.session.commit()
    flash(f'Book issued to {reservation.user.username}. Due date: {due_date.strftime("%Y-%m-%d")}', 'success')
    return redirect(url_for('librarian.manage_reservations'))

@librarian_bp.route('/cancel_reservation/<int:reservation_id>')
@login_required
@librarian_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.status = 'cancelled'
    db.session.commit()
    flash('Reservation cancelled.', 'info')
    return redirect(url_for('librarian.manage_reservations'))

@librarian_bp.route('/return', methods=['GET', 'POST'])
@login_required
@librarian_required
def return_book():
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        # Find active transaction for this book (assuming one copy per ISBN for simplicity, or find by User+ISBN)
        # Better: Search by User Email + ISBN or just Username
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('librarian.return_book'))
            
        # Find transactions for this user
        transactions = Transaction.query.filter_by(user_id=user.id, status='issued').all()
        return render_template('librarian/return_book.html', transactions=transactions, user=user)
        
    return render_template('librarian/return_book.html', transactions=None)

@librarian_bp.route('/return_confirm/<int:transaction_id>')
@login_required
@librarian_required
def confirm_return(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    transaction.return_date = datetime.utcnow()
    transaction.status = 'returned'
    
    # Calculate Fine (Simple logic: $1 per day overdue)
    if transaction.return_date > transaction.due_date:
        overdue_days = (transaction.return_date - transaction.due_date).days
        transaction.fine_amount = overdue_days * 1.0
        flash(f'Book returned. Overdue by {overdue_days} days. Fine: ${transaction.fine_amount}', 'warning')
    else:
        flash('Book returned on time.', 'success')
        
    # Update stock
    transaction.book.available_count += 1
    
    db.session.commit()
    return redirect(url_for('librarian.return_book'))
