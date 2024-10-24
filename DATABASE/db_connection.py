from flask import Flask
from DAL.dal import db

def init_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = init_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

