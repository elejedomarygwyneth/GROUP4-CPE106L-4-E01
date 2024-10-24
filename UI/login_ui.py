import tkinter as tk
from tkinter import ttk, messagebox
from UI.dashboard_ui import open_dashboard
from PAL.login_pal import login_user

def open_login():
    """Launch the login window."""
    root = tk.Tk()
    root.title("EventSynch - Login")
    root.geometry("400x300")
    root.configure(bg="#e8f4f8")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TLabel", font=("Arial", 12), background="#e8f4f8")

    # Title
    ttk.Label(root, text="Welcome to EventSynch", font=("Arial", 18, "bold")).pack(pady=10)

    # Username and Password Fields
    ttk.Label(root, text="Username").pack(pady=5)
    entry_username = ttk.Entry(root, width=30)
    entry_username.pack(pady=5)

    ttk.Label(root, text="Password").pack(pady=5)
    entry_password = ttk.Entry(root, width=30, show="*")
    entry_password.pack(pady=5)

    # Login Button
    def login():
        username = entry_username.get()
        password = entry_password.get()
        if login_user(username, password):
            messagebox.showinfo("Success", "Login Successful")
            root.destroy()
            open_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    ttk.Button(root, text="Login", command=login).pack(pady=20)

    root.mainloop()
