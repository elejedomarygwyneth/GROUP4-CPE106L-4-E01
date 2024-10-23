events = []

def add_event(event_name, event_date):
    event = {"name": event_name, "date": event_date}
    events.append(event)
    return event

def edit_event(event_name, new_name, new_date):
    for event in events:
        if event["name"] == event_name:
            event["name"] = new_name
            event["date"] = new_date
            return event
    return None
