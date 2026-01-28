from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.decorators import admin_required
from app.models import User, Book, Transaction
from app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_books': Book.query.count(),
        'total_users': User.query.filter(User.role != 'admin').count(),
        'issued_books': Transaction.query.filter_by(status='issued').count(),
        'overdue_books': Transaction.query.filter_by(status='overdue').count()
    }
    recent_transactions = Transaction.query.order_by(Transaction.issued_date.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, transactions=recent_transactions)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/users/promote/<int:user_id>')
@login_required
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'user':
        user.role = 'librarian'
        db.session.commit()
        flash(f'User {user.username} promoted to Librarian.', 'success')
    elif user.role == 'librarian':
        user.role = 'user'
        db.session.commit()
        flash(f'User {user.username} demoted to User.', 'info')
    return redirect(url_for('admin.manage_users'))
@admin_bp.route('/sales')
@login_required
@admin_required
def sales_report():
    # Fetch all completed purchase transactions
    sales = Transaction.query.filter_by(transaction_type='purchase', status='completed').order_by(Transaction.issued_date.desc()).all()
    total_revenue = sum(sale.amount for sale in sales)
    return render_template('admin/sales_report.html', sales=sales, total_revenue=total_revenue)
