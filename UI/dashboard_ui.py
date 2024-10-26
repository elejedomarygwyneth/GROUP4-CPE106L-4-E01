import tkinter as tk
from tkinter import ttk, messagebox
from BL.event_management import add_event, delete_event, get_all_events, update_event

event_window_open = None
window_size = "800x600"  # Set uniform window size for dashboard and event list windows

def open_dashboard(username):
    """Launch the event management dashboard."""
    dashboard = tk.Tk()
    dashboard.title(f"EventSynch Dashboard - Welcome {username}")
    dashboard.geometry(window_size)
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
        add_window.geometry("400x350")
        add_window.resizable(False, False)

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

        def save_event():
            """Save the new event."""
            add_event(
                event_name.get(), 
                event_date.get(), 
                event_location.get(), 
                event_description.get(), 
                username
            )
            messagebox.showinfo("Success", "Event Added")
            add_window.destroy()

        def cancel_event():
            """Prompt confirmation before closing the add event window without saving."""
            if any(field.get() for field in [event_name, event_date, event_location, event_description]):
                confirm = messagebox.askyesno(
                    "Cancel Confirmation",
                    "You have unsaved changes. Are you sure you want to cancel? Your data will not be saved."
                )
                if not confirm:
                    return
            add_window.destroy()

        # Create a frame to hold the Save and Cancel buttons side by side
        button_frame = ttk.Frame(add_window)
        button_frame.pack(pady=10)

        # Place the Save and Cancel buttons side by side within the frame
        ttk.Button(button_frame, text="Save", command=save_event).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_event).pack(side="left", padx=5)

    ttk.Button(event_tab, text="Add Event", command=open_add_event).pack(pady=10)

    def open_event_list_window():
        global event_window_open  
        if event_window_open is None:  
            dashboard.withdraw()

            event_window_open = tk.Toplevel(dashboard)
            event_window_open.title("All Events")
            event_window_open.geometry(window_size)
            event_window_open.resizable(False, False)

            def on_close():
                global event_window_open
                event_window_open.destroy()
                event_window_open = None
                dashboard.deiconify()

            event_window_open.protocol("WM_DELETE_WINDOW", on_close)

            # Add a scrollable canvas
            canvas = tk.Canvas(event_window_open)
            scrollbar = ttk.Scrollbar(event_window_open, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            def refresh_event_list():
                for widget in scrollable_frame.winfo_children():
                    widget.destroy()

                events = get_all_events(username)
                if not events:
                    ttk.Label(scrollable_frame, text="No events found.", justify='center').pack(pady=20)
                    ttk.Button(scrollable_frame, text="Back", command=on_close).pack(pady=10)
                    return

                for event in events:
                    event_frame = ttk.Frame(scrollable_frame, relief="groove", borderwidth=2)
                    event_frame.pack(fill="x", pady=10, padx=20)

                    event_info = (
                        f"Event: {event['name']}\n"
                        f"Date: {event['date']}\n"
                        f"Location: {event['location']}\n"
                        f"Description: {event['description']}"
                    )
                    ttk.Label(event_frame, text=event_info, justify='center').pack(pady=5)

                    # Function to delete event
                    def delete_event_action(event_id=event['id']):
                        response = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this event?")
                        if response:
                            delete_event(event_id)
                            refresh_event_list()

                    # Function to edit event
                    def edit_event(event_data=event):
                        edit_window = tk.Toplevel(event_window_open)
                        edit_window.title("Edit Event")
                        edit_window.geometry("400x350")
                        edit_window.resizable(False, False)

                        # Populate fields with current event data
                        ttk.Label(edit_window, text="Event Name").pack(pady=5)
                        event_name = ttk.Entry(edit_window)
                        event_name.insert(0, event_data['name'])
                        event_name.pack(pady=5)

                        ttk.Label(edit_window, text="Event Date (MM-DD-YYYY)").pack(pady=5)
                        event_date = ttk.Entry(edit_window)
                        event_date.insert(0, event_data['date'])
                        event_date.pack(pady=5)

                        ttk.Label(edit_window, text="Location").pack(pady=5)
                        event_location = ttk.Entry(edit_window)
                        event_location.insert(0, event_data['location'])
                        event_location.pack(pady=5)

                        ttk.Label(edit_window, text="Description").pack(pady=5)
                        event_description = ttk.Entry(edit_window)
                        event_description.insert(0, event_data['description'])
                        event_description.pack(pady=5)

                        def save_edited_event():
                            updated_event = {
                                'id': event_data['id'],
                                'name': event_name.get(),
                                'date': event_date.get(),
                                'location': event_location.get(),
                                'description': event_description.get()
                            }
                            if update_event(updated_event):
                                messagebox.showinfo("Success", "Event updated successfully")
                                edit_window.destroy()
                                refresh_event_list()
                            else:
                                messagebox.showerror("Error", "Failed to update event")

                        def cancel_edit():
                            if (event_name.get() != event_data['name'] or
                                    event_date.get() != event_data['date'] or
                                    event_location.get() != event_data['location'] or
                                    event_description.get() != event_data['description']):
                                confirm = messagebox.askyesno(
                                    "Cancel Confirmation",
                                    "You have unsaved changes. Are you sure you want to cancel? Your changes will not be saved."
                                )
                                if not confirm:
                                    return
                            edit_window.destroy()

                        # Frame for Save and Cancel buttons
                        button_frame = ttk.Frame(edit_window)
                        button_frame.pack(pady=10)

                        # Place Save and Cancel buttons side by side
                        ttk.Button(button_frame, text="Save Changes", command=save_edited_event).pack(side="left", padx=5)
                        ttk.Button(button_frame, text="Cancel", command=cancel_edit).pack(side="left", padx=5)

                    # Center the Delete and Edit buttons within each event frame
                    button_frame = ttk.Frame(event_frame)
                    button_frame.pack(pady=5)
                    ttk.Button(button_frame, text="Delete", command=delete_event_action).pack(side="left", padx=5)
                    ttk.Button(button_frame, text="Edit", command=edit_event).pack(side="left", padx=5)

                ttk.Button(scrollable_frame, text="Back", command=on_close).pack(pady=10)

            refresh_event_list()

    ttk.Button(event_tab, text="View All Events", command=open_event_list_window).pack(pady=10)

    def confirm_logout():
        if messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
            dashboard.destroy()

    ttk.Button(dashboard, text="Logout", command=confirm_logout).pack(pady=10)
    dashboard.mainloop()
