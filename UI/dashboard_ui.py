import tkinter as tk
from tkinter import ttk, messagebox
import re
from BL.event_management import add_event, delete_event, get_all_events, update_event, update_financials, get_financials

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

            if not is_valid_date(event_date_val):
                messagebox.showerror("Error", "Invalid date format. Please use MM-DD-YYYY.")
                return

            add_event(
                event_name_val,
                event_date_val,
                event_location_val,
                event_description_val,
                username
            )
            messagebox.showinfo("Success", "Event Added")
            add_window.destroy()

        # Button frame for Save and Cancel buttons
        button_frame = ttk.Frame(add_window)
        button_frame.pack(pady=10)

        # Save and Cancel buttons
        ttk.Button(button_frame, text="Save", command=save_event).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=add_window.destroy).pack(side="left", padx=5)

    ttk.Button(event_tab, text="Add Event", command=open_add_event).pack(pady=10)

    def open_event_list_window():
        """Open a new window for viewing all events and close the dashboard."""
        dashboard.withdraw()

        event_window = tk.Toplevel(dashboard)
        event_window.title("All Events")
        event_window.geometry("600x400")
        event_window.configure(bg="#f0f0f0")

        # Center the event window
        event_window.update_idletasks()
        x = (event_window.winfo_screenwidth() // 2) - (event_window.winfo_width() // 2)
        y = (event_window.winfo_screenheight() // 2) - (event_window.winfo_height() // 2)
        event_window.geometry(f"+{x}+{y}")

        # Canvas and scrollbar for event window
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
            event_window.destroy()
            dashboard.deiconify()

        event_window.protocol("WM_DELETE_WINDOW", on_close)

        refresh_event_list(scrollable_frame, event_window)

    def refresh_event_list(scrollable_frame, event_window):
        """Show all events and make them clickable to edit or delete."""
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        events = get_all_events(username)
        if not events:
            ttk.Label(scrollable_frame, text="No events found.", font=("Arial", 14)).pack(pady=20, padx=20)
            ttk.Button(scrollable_frame, text="Back", command=lambda: go_back(event_window)).pack(pady=20)
            return

        for event in events:
            event_frame = ttk.Frame(scrollable_frame, relief="groove", borderwidth=2, padding=10)
            event_frame.pack(pady=10)

            ttk.Label(event_frame, text=f"Event: {event['name']}", font=("Arial", 14, "bold")).pack(anchor='center')
            ttk.Label(event_frame, text=f"Date: {event['date']}", font=("Arial", 12)).pack(anchor='center')
            ttk.Label(event_frame, text=f"Location: {event['location']}", font=("Arial", 12)).pack(anchor='center')

            event_frame.bind("<Button-1>", lambda e, ev=event: open_financial_tracker(ev, event_window))

            button_frame = ttk.Frame(event_frame)
            button_frame.pack(pady=5)

            ttk.Button(button_frame, text="Edit", command=lambda e=event: edit_event_details(e, scrollable_frame, event_window)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Delete", command=lambda e=event['id']: confirm_delete(e, scrollable_frame, event_window)).pack(side="right", padx=5)

        # Center the back button
        ttk.Button(scrollable_frame, text="Back", command=lambda: go_back(event_window)).pack(pady=20)

    def go_back(event_window):
        """Close the event window and re-open the dashboard."""
        event_window.destroy()
        dashboard.deiconify()

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
                update_event(event['id'], updated_name, updated_date, updated_location, updated_description)
                messagebox.showinfo("Success", "Event details updated")
                refresh_event_list(scrollable_frame, event_window)
                edit_window.destroy()

        button_frame = ttk.Frame(edit_window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Save", command=save_event_details).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side="left", padx=5)

    def open_financial_tracker(event, event_window):
        """Open the financial tracker for the selected event."""
        event_window.withdraw()  # Hide the event list window

        financial_window = tk.Toplevel(event_window)
        financial_window.title(f"Financial Tracker for {event['name']}")
        financial_window.geometry("600x500")

        # Center the financial tracker window
        financial_window.update_idletasks()
        x = (financial_window.winfo_screenwidth() // 2) - (financial_window.winfo_width() // 2)
        y = (financial_window.winfo_screenheight() // 2) - (financial_window.winfo_height() // 2)
        financial_window.geometry(f"+{x}+{y}")

        # Budget input
        ttk.Label(financial_window, text="Set Budget").pack(pady=10)
        budget_entry = ttk.Entry(financial_window, font=("Arial", 12), width=20)
        budget_entry.pack(pady=10, padx=20)

        # Expense tracking area
        categories_frame = ttk.Frame(financial_window)
        categories_frame.pack(pady=10)

        # Table header (only shown when adding expenses)
        ttk.Label(categories_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(categories_frame, text="Vendor").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(categories_frame, text="Description").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(categories_frame, text="Amount").grid(row=0, column=3, padx=5, pady=5)

        expenses = []  # To hold expense entries
        total_expenses = 0.0

        def add_expense_row():
            """Add a new expense row."""
            row = len(expenses) + 1
            date_entry = ttk.Entry(categories_frame)
            date_entry.grid(row=row, column=0, padx=5, pady=5)
            vendor_entry = ttk.Entry(categories_frame)
            vendor_entry.grid(row=row, column=1, padx=5, pady=5)
            description_entry = ttk.Entry(categories_frame)
            description_entry.grid(row=row, column=2, padx=5, pady=5)
            amount_entry = ttk.Entry(categories_frame)
            amount_entry.grid(row=row, column=3, padx=5, pady=5)

            expenses.append((date_entry, vendor_entry, description_entry, amount_entry))

        # Add button for adding expenses
        ttk.Button(financial_window, text="Add Expense", command=add_expense_row).pack(pady=5)

        # Summary area for budget, total expenses, and remaining balance
        summary_frame = ttk.Frame(financial_window)
        summary_frame.pack(pady=10)

        ttk.Label(summary_frame, text="Total Budget:").grid(row=0, column=0, sticky="w")
        total_budget_label = ttk.Label(summary_frame, text="₱0.00")
        total_budget_label.grid(row=0, column=1, sticky="w")

        ttk.Label(summary_frame, text="Total Expenses:").grid(row=1, column=0, sticky="w")
        total_expenses_label = ttk.Label(summary_frame, text="₱0.00")
        total_expenses_label.grid(row=1, column=1, sticky="w")

        remaining_balance_label = ttk.Label(summary_frame, text="₱0.00")
        ttk.Label(summary_frame, text="Remaining Balance:").grid(row=2, column=0, sticky="w")
        remaining_balance_label.grid(row=2, column=1, sticky="w")

        def save_financial_details():
            """Save budget and expenses for the event."""
            budget = budget_entry.get()

            try:
                budget_float = float(budget)  # Convert budget to float
                total_expenses = 0.0

                # Calculate total expenses from the input rows
                for date_entry, vendor_entry, description_entry, amount_entry in expenses:
                    try:
                        date = date_entry.get()
                        vendor = vendor_entry.get()
                        description = description_entry.get()
                        amount = amount_entry.get()

                        # Ensure that each entry is valid before processing
                        if date and vendor and description and amount:
                            try:
                                amount_float = float(amount)
                                total_expenses += amount_float  # Add the expense amount to total expenses
                            except ValueError:
                                messagebox.showerror("Error", f"Invalid amount value: {amount}. Please enter a valid number.")
                                return
                    except IndexError:
                        # Skip rows that do not have complete data
                        continue

                remaining_balance = budget_float - total_expenses

                # Update the labels to display formatted values
                total_budget_label.config(text=f"₱{budget_float:,.2f}")
                total_expenses_label.config(text=f"₱{total_expenses:,.2f}")
                remaining_balance_label.config(text=f"₱{remaining_balance:,.2f}")

                # Save financial data
                update_financials(event['id'], budget_float, expenses)

                messagebox.showinfo("Success", f"Budget set to ₱{budget_float:,.2f} and expenses recorded.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for the budget.")
                return

        # Button frame to group Save, Cancel, and Back buttons
        button_frame = ttk.Frame(financial_window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Save", command=save_financial_details).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=financial_window.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Back", command=lambda: (financial_window.destroy(), event_window.deiconify())).pack(side="right", padx=5)

    # Add Event and View All Events buttons
    ttk.Button(event_tab, text="View All Events", command=open_event_list_window).pack(pady=10)

    # Logout Button
    def logout():
        dashboard.destroy()  # Close the dashboard window

    ttk.Button(dashboard, text="Logout", command=logout).pack(pady=10)

    dashboard.mainloop()
