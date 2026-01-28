from app import create_app, db
from app.models import User, Book, Transaction, Reservation

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Book': Book, 'Transaction': Transaction, 'Reservation': Reservation}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a default admin if none exists
        if not User.query.filter_by(role='admin').first():
            admin = User(username='admin', email='admin@library.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: email=admin@library.com, password=admin123")
            
    app.run(debug=True)
