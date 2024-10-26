from DAL.dal import db, Event
from DATABASE.db_connection import init_app  # Import your Flask app initializer

app = init_app()  # Initialize the Flask app

def add_event(name, date, location, description, user_id):
    """Add an event within the application context."""
    with app.app_context():
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
    """Delete an event by ID."""
    with app.app_context():
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()

def get_all_events(user_id):
    """Retrieve all events for a specific user."""
    with app.app_context():
        events = Event.query.filter_by(user_id=user_id).all()
        return [
            {
                "id": e.id,
                "name": e.name,
                "date": e.date,
                "location": e.location,
                "description": e.description
            }
            for e in events
        ]

def update_event(updated_event):
    """Update an existing event with new data.
    
    Args:
        updated_event (dict): A dictionary containing the updated event data, including the event ID.
            Example format:
            {
                'id': event_id,
                'name': 'Updated Event Name',
                'date': 'MM-DD-YYYY',
                'location': 'Updated Location',
                'description': 'Updated Description'
            }
    """
    event_id = updated_event.get("id")
    if not isinstance(event_id, int):
        raise ValueError("event_id must be an integer.")

    with app.app_context():
        event = Event.query.get(event_id)
        if event:
            # Update fields only if new values are provided
            event.name = updated_event.get("name", event.name)
            event.date = updated_event.get("date", event.date)
            event.location = updated_event.get("location", event.location)
            event.description = updated_event.get("description", event.description)
            db.session.commit()
            return True
        return False  # Event not found
