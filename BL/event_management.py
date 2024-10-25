from DAL.dal import db, Event
from DATABASE.db_connection import init_app

app = init_app()

def add_event(name, date, location, description, user_id):
    """Add an event within the application context."""
    print(f"Adding event to DB: Name={name}, Date={date}, Location={location}, Description={description}, User ID={user_id}")
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
    print("Event added to DB successfully.")

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
                "description": e.description,
                "budget": getattr(e, 'budget', 0),  
                "expenses": getattr(e, 'expenses', [])  
            }
            for e in events
        ]

def update_event(event_id, name=None, date=None, location=None, description=None, budget=None, expenses=None):
    """Update event details (name, date, location, description) and optionally financials."""
    with app.app_context():
        event = Event.query.get(event_id)
        if event:
            if name is not None:
                event.name = name
            if date is not None:
                event.date = date
            if location is not None:
                event.location = location
            if description is not None:
                event.description = description

            if budget is not None:
                event.budget = budget
            if expenses is not None:
                event.expenses = expenses

            db.session.commit()
            print(f"Event {event_id} updated successfully.")
