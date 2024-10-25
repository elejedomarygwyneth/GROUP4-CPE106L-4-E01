import tkinter as tk
from tkinter import ttk, messagebox
import re  # Import the re module for date validation
from BL.event_management import add_event, delete_event, get_all_events, update_event

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

        # Event details
        ttk.Label(add_window, text="Event Name").pack(pady=5)
        event_name = ttk.Entry(add_window)
        event_name.pack(pady=5)

        ttk.Label(add_window, text="Event Date (MM-DD-YYYY)").pack(pady=5)
        event_date = ttk.Entry(add_window)
        event_date.pack(pady=5)

        ttk.Label(add_window, text="Location").pack(pady=5)
        event_location = ttk.Entry(add_window)
        event_location.pack(pady=5)

        ttk.Label(add_window, text="Description").pack(pady=5)
        event_description = ttk.Entry(add_window)
        event_description.pack(pady=5)

        def is_valid_date(date_str):
            """Validate the date format (MM-DD-YYYY)."""
            pattern = r'^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-\d{4}$'
            return re.match(pattern, date_str) is not None

        def save_event():
            """Save a new event."""
            event_name_val = event_name.get()
            event_date_val = event_date.get()
            event_location_val = event_location.get()
            event_description_val = event_description.get()

            print(f"Attempting to save event with: Name={event_name_val}, Date={event_date_val}, Location={event_location_val}, Description={event_description_val}")
            
            if not is_valid_date(event_date_val):
                messagebox.showerror("Error", "Invalid date format. Please use MM-DD-YYYY.")
                return

            # Save the event without budget and expenses
            add_event(
                event_name_val,
                event_date_val,
                event_location_val,
                event_description_val,
                username
            )
            print("Event saved successfully.")
            messagebox.showinfo("Success", "Event Added")
            add_window.destroy()

        # Button frame to group Save and Cancel buttons
        button_frame = ttk.Frame(add_window)
        button_frame.pack(pady=10)

        # Save and Cancel buttons
        ttk.Button(button_frame, text="Save", command=save_event).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=add_window.destroy).pack(side="left", padx=5)

    ttk.Button(event_tab, text="Add Event", command=open_add_event).pack(pady=10)

    def open_event_list_window():
        """Open a new window for viewing all events and close the dashboard."""
        dashboard.withdraw()  # Hide the dashboard

        event_window = tk.Toplevel(dashboard)
        event_window.title("All Events")
        event_window.geometry("600x400")
        event_window.configure(bg="#f0f0f0")  # Light gray background

        # Add a canvas and scrollbar to the new event window
        canvas = tk.Canvas(event_window)
        scrollbar = ttk.Scrollbar(event_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_close():
            event_window.destroy()  # Close event window
            dashboard.deiconify()  # Show the dashboard again

        event_window.protocol("WM_DELETE_WINDOW", on_close)

        refresh_event_list(scrollable_frame, event_window)

    def refresh_event_list(scrollable_frame, event_window):
        """Show all events and make them clickable to edit or delete."""
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        events = get_all_events(username)
        if not events:
            # Center the "No events found" message and the Back button
            ttk.Label(scrollable_frame, text="No events found.", font=("Arial", 14)).pack(pady=20, padx=20)
            ttk.Button(scrollable_frame, text="Back", command=lambda: go_back(event_window)).pack(pady=20)
            return

        for event in events:
            event_frame = ttk.Frame(scrollable_frame, relief="groove", borderwidth=2, padding=10)
            event_frame.pack(pady=10, padx=150)  # Center the event frame with horizontal padding

            ttk.Label(event_frame, text=f"Event: {event['name']}", font=("Arial", 14, "bold")).pack(anchor='center')
            ttk.Label(event_frame, text=f"Date: {event['date']}", font=("Arial", 12)).pack(anchor='center')
            ttk.Label(event_frame, text=f"Location: {event['location']}", font=("Arial", 12)).pack(anchor='center')
            ttk.Label(event_frame, text=f"Budget: ₱{event.get('budget', 0):.2f}", font=("Arial", 12)).pack(anchor='center')

            # Edit button for editing event details (name, date, etc.)
            ttk.Button(event_frame, text="Edit", command=lambda e=event: edit_event_details(e, scrollable_frame, event_window)).pack(side="left", padx=5, pady=5)

            # Delete button with confirmation prompt
            ttk.Button(event_frame, text="Delete", command=lambda e=event['id']: confirm_delete(e, scrollable_frame, event_window)).pack(side="right", padx=5, pady=5)

        # Center the back button when events are available
        ttk.Button(scrollable_frame, text="Back", command=lambda: go_back(event_window)).pack(pady=20)

    def go_back(event_window):
        """Close the event window and re-open the dashboard."""
        event_window.destroy()
        dashboard.deiconify()  # Re-open the dashboard when back is pressed

    def confirm_delete(event_id, scrollable_frame, event_window):
        """Ask for confirmation before deleting an event."""
        confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this event?")
        if confirm:
            delete_event(event_id)
            refresh_event_list(scrollable_frame, event_window)

    def edit_event_details(event, scrollable_frame, event_window):
        """Open a window to edit event details (name, date, location, description)."""
        edit_window = tk.Toplevel(dashboard)
        edit_window.title(f"Edit Event: {event['name']}")
        edit_window.geometry("400x400")

        # Editable fields for event details
        ttk.Label(edit_window, text="Event Name").pack(pady=5)
        event_name = ttk.Entry(edit_window)
        event_name.pack(pady=5)
        event_name.insert(0, event['name'])

        ttk.Label(edit_window, text="Event Date (MM-DD-YYYY)").pack(pady=5)
        event_date = ttk.Entry(edit_window)
        event_date.pack(pady=5)
        event_date.insert(0, event['date'])

        ttk.Label(edit_window, text="Location").pack(pady=5)
        event_location = ttk.Entry(edit_window)
        event_location.pack(pady=5)
        event_location.insert(0, event['location'])

        ttk.Label(edit_window, text="Description").pack(pady=5)
        event_description = ttk.Entry(edit_window)
        event_description.pack(pady=5)
        event_description.insert(0, event['description'])

        def is_valid_date(date_str):
            """Validate the date format (MM-DD-YYYY)."""
            pattern = r'^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-\d{4}$'
            return re.match(pattern, date_str) is not None

        def save_event_details():
            """Prompt confirmation, then save the edited event details."""
            updated_name = event_name.get()
            updated_date = event_date.get()
            updated_location = event_location.get()
            updated_description = event_description.get()

            if not is_valid_date(updated_date):
                messagebox.showerror("Error", "Invalid date format. Please use MM-DD-YYYY.")
                return

            confirm = messagebox.askyesno("Save Confirmation", "Are you sure you want to save the changes?")
            if confirm:
                # Assuming we use update_event to save details like name, date, location, and description
                update_event(event['id'], updated_name, updated_date, updated_location, updated_description)
                messagebox.showinfo("Success", "Event details updated")
                refresh_event_list(scrollable_frame, event_window)
                edit_window.destroy()

        # Button frame to group Save and Cancel buttons for editing
        button_frame = ttk.Frame(edit_window)
        button_frame.pack(pady=10)

        # Save and Cancel buttons for editing event
        ttk.Button(button_frame, text="Save", command=save_event_details).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side="left", padx=5)

    ttk.Button(event_tab, text="View All Events", command=open_event_list_window).pack(pady=10)

    # Add the logout button to the dashboard, placed under the tabs
    ttk.Button(dashboard, text="Logout", command=dashboard.destroy).pack(pady=10)

    dashboard.mainloop()
