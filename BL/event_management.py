from DAL.dal import db, Event

def add_event(event_name, event_date, location, description, user_id):
    event = Event(
        name=event_name, date=event_date, location=location, 
        description=description, user_id=user_id
    )
    db.session.add(event)
    db.session.commit()
    return event

def edit_event(event_id, new_name, new_date, new_location, new_description):
    event = Event.query.get(event_id)
    if event:
        event.name = new_name
        event.date = new_date
        event.location = new_location
        event.description = new_description
        db.session.commit()
        return event
    return None

def get_all_events(user_id):
    return Event.query.filter_by(user_id=user_id).all()



