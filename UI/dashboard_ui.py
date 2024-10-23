import tkinter as tk
from tkinter import messagebox
from PAL.event_pal import create_event

def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("EventSynch Dashboard")
    dashboard.geometry("400x300")

    tk.Label(dashboard, text="Welcome to EventSynch!").pack(pady=10)

    tk.Button(dashboard, text="Add Event", command=add_event).pack(pady=10)
    tk.Button(dashboard, text="Logout", command=dashboard.destroy).pack(pady=10)

    dashboard.mainloop()

def add_event():
    add_window = tk.Toplevel()
    add_window.title("Add Event")
    add_window.geometry("300x200")

    tk.Label(add_window, text="Event Name").pack(pady=10)
    event_name = tk.Entry(add_window)
    event_name.pack()

    tk.Label(add_window, text="Event Date").pack(pady=10)
    event_date = tk.Entry(add_window)
    event_date.pack()

    tk.Button(add_window, text="Save", command=lambda: save_event(event_name.get(), event_date.get())).pack(pady=10)

def save_event(name, date):
    if name and date:
        create_event(name, date)
        messagebox.showinfo("Event Saved", f"Event '{name}' on {date} saved!")
    else:
        messagebox.showerror("Error", "Please provide valid inputs for the event")

