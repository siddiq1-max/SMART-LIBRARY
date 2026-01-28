from flask import Blueprint, render_template
from app.models import Book
from app import db
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Fetch Collections
    new_releases = Book.query.order_by(Book.created_at.desc()).limit(10).all()
    top_rated = Book.query.order_by(Book.average_rating.desc()).limit(10).all()
    
    # Recommended (Random for now, or algorithm later)
    all_books = Book.query.all()
    recommended = random.sample(all_books, min(len(all_books), 10)) if all_books else []
    
    # Categories
    categories = [r[0] for r in db.session.query(Book.category).distinct().all()]
    
    return render_template('index.html', 
                           new_releases=new_releases, 
                           top_rated=top_rated, 
                           recommended=recommended, 
                           categories=categories)
