import tkinter as tk
from tkinter import ttk, messagebox
from BL.event_management import add_event, delete_event, get_all_events

event_window_open = None

def open_dashboard(username):
    """Launch the event management dashboard."""
    dashboard = tk.Tk()
    dashboard.title(f"EventSynch Dashboard - Welcome {username}")
    dashboard.geometry("800x600")
    dashboard.configure(bg="#e8f4f8")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TLabel", font=("Arial", 12), background="#e8f4f8")

    ttk.Label(dashboard, text=f"Welcome to EventSynch, {username}!", font=("Arial", 18, "bold")).pack(pady=10)

    tabs = ttk.Notebook(dashboard)
    tabs.pack(expand=1, fill="both")

    event_tab = ttk.Frame(tabs)
    tabs.add(event_tab, text="Event Management")

    def open_add_event():
        """Open a window to add a new event."""
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
            """Save a new event."""
            add_event(
                event_name.get(), 
                event_date.get(), 
                event_location.get(), 
                event_description.get(), 
                username
            )
            messagebox.showinfo("Success", "Event Added")
            add_window.destroy()

        ttk.Button(add_window, text="Save", command=save_event).pack(pady=10)

    ttk.Button(event_tab, text="Add Event", command=open_add_event).pack(pady=10)

    def open_event_list_window():
        global event_window_open  
        if event_window_open is None:  
        
            dashboard.withdraw()

            event_window_open = tk.Toplevel(dashboard)
            event_window_open.title("All Events")
            event_window_open.geometry("600x400")

            def on_close():
                global event_window_open
                event_window_open.destroy()
                event_window_open = None
                
                dashboard.deiconify()

            event_window_open.protocol("WM_DELETE_WINDOW", on_close)

           
            def refresh_event_list():
                for widget in event_window_open.winfo_children():
                    widget.destroy()

                events = get_all_events(username)
                if not events:
                    ttk.Label(event_window_open, text="No events found.", justify='center').pack(pady=20)
                    ttk.Button(event_window_open, text="Back", command=on_close).pack(pady=10)
                    return

                for event in events:
                    event_frame = ttk.Frame(event_window_open, relief="groove", borderwidth=2)
                    event_frame.pack(fill="x", pady=5, padx=10)

                    event_info = f"Event: {event['name']}\nDate: {event['date']}\nLocation: {event['location']}\nDescription: {event['description']}"
                    ttk.Label(event_frame, text=event_info, justify='left').pack(pady=5)

                    def delete_event_action(event_id=event['id']):
                        """Delete the event with confirmation."""
                        response = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this event?")
                        if response:
                            delete_event(event_id)
                            refresh_event_list()  

                    ttk.Button(event_frame, text="Delete", command=delete_event_action).pack(pady=5)

                ttk.Button(event_window_open, text="Back", command=on_close).pack(pady=10)

            refresh_event_list() 

    ttk.Button(event_tab, text="View All Events", command=open_event_list_window).pack(pady=10)

    ttk.Button(dashboard, text="Logout", command=dashboard.destroy).pack(pady=10)
    dashboard.mainloop()
