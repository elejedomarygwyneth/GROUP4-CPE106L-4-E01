from flask import Flask
from DAL.dal import db, Event

def init_app():
    """Initialize the Flask application and create the database."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        # Create all tables
        db.create_all()

    return app

if __name__ == "__main__":
    app = init_app()
    print("Database initialized successfully.")



