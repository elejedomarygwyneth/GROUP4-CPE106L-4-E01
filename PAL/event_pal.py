from bl.event_management import add_event, edit_event

def create_event(event_name, event_date):
    return add_event(event_name, event_date)

def update_event(event_name, new_name, new_date):
    return edit_event(event_name, new_name, new_date)
