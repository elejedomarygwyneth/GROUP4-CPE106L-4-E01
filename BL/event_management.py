from DAL.dal import db, Event
from DATABASE.db_connection import init_app  # Ensure you import your Flask app

app = init_app()  # Initialize the Flask app

def add_event(name, date, location, description, user_id):
    with app.app_context():  # Ensure the operation runs within the app context
        event = Event(
            name=name, 
            date=date, 
            location=location, 
            description=description, 
            user_id=user_id
        )
        db.session.add(event)
        db.session.commit()

def delete_event(event_id):
    with app.app_context():
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()

def get_all_events(user_id):
    with app.app_context():
        events = Event.query.filter_by(user_id=user_id).all()
        return [
            {"id": e.id, "name": e.name, "date": e.date, "location": e.location, "description": e.description}
            for e in events
        ]

