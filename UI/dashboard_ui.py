import tkinter as tk
from tkinter import ttk, messagebox
from BL.event_management import add_event, delete_event, get_all_events

def open_dashboard(username):
    """Launch the event management dashboard."""
    dashboard = tk.Tk()
    dashboard.title(f"EventSynch Dashboard - Welcome {username}")
    dashboard.geometry("600x500")
    dashboard.configure(bg="#e8f4f8")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TLabel", font=("Arial", 12), background="#e8f4f8")

    # Title
    ttk.Label(dashboard, text=f"Welcome to EventSynch, {username}!", font=("Arial", 18, "bold")).pack(pady=10)

    # Event List Section
    events_frame = ttk.Frame(dashboard)
    events_frame.pack(pady=10)

    def refresh_events():
        for widget in events_frame.winfo_children():
            widget.destroy()
        events = get_all_events(username)
        for event in events:
            event_info = f"{event['name']} | {event['date']} | {event['location']} | {event['description']}"
            ttk.Label(events_frame, text=event_info).pack()
            ttk.Button(events_frame, text="Delete", command=lambda e=event['id']: delete_event(e)).pack()

    refresh_events()

    # Add Event Button
    def open_add_event():
        add_window = tk.Toplevel(dashboard)
        add_window.title("Add Event")
        add_window.geometry("400x300")

        ttk.Label(add_window, text="Event Name").pack(pady=5)
        event_name = ttk.Entry(add_window)
        event_name.pack(pady=5)

        ttk.Label(add_window, text="Event Date").pack(pady=5)
        event_date = ttk.Entry(add_window)
        event_date.pack(pady=5)

        ttk.Label(add_window, text="Location").pack(pady=5)
        event_location = ttk.Entry(add_window)
        event_location.pack(pady=5)

        ttk.Label(add_window, text="Description").pack(pady=5)
        event_description = ttk.Entry(add_window)
        event_description.pack(pady=5)

        def save_event():
            add_event(
                event_name.get(),
                event_date.get(),
                event_location.get(),
                event_description.get(),
                username
            )
            messagebox.showinfo("Success", "Event Added")
            add_window.destroy()
            refresh_events()

        ttk.Button(add_window, text="Save", command=save_event).pack(pady=10)

    ttk.Button(dashboard, text="Add Event", command=open_add_event).pack(pady=10)

    ttk.Button(dashboard, text="Logout", command=dashboard.destroy).pack(pady=10)

    dashboard.mainloop()
