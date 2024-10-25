import tkinter as tk
from tkinter import ttk, messagebox
from UI.dashboard_ui import open_dashboard
from PAL.login_pal import login_user

def open_login_form():
    """Displays the login form."""
    welcome_window.destroy()

    login_window = tk.Tk()
    login_window.title("EventSynch - Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#e8f4f8")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TLabel", font=("Arial", 12), background="#e8f4f8")

    ttk.Label(login_window, text="Login to EventSynch", font=("Arial", 18, "bold")).pack(pady=10)

    ttk.Label(login_window, text="Username").pack(pady=5)
    entry_username = ttk.Entry(login_window, width=30)
    entry_username.pack(pady=5)

    ttk.Label(login_window, text="Password").pack(pady=5)
    entry_password = ttk.Entry(login_window, width=30, show="*")
    entry_password.pack(pady=5)

    def login():
        username = entry_username.get()
        password = entry_password.get()
        if login_user(username, password):
            messagebox.showinfo("Success", "Login Successful")
            login_window.destroy()
            open_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

    ttk.Button(login_window, text="Login", command=login).pack(pady=20)

    login_window.mainloop()

def open_welcome_window():
    """Displays the welcome window with a 'Get Started' button."""
    global welcome_window  

    welcome_window = tk.Tk()
    welcome_window.title("Welcome to EventSynch!")
    welcome_window.geometry("400x300")
    welcome_window.configure(bg="#e8f4f8")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 14), padding=5)
    style.configure("TLabel", font=("Arial", 16), background="#e8f4f8", foreground="black")

    ttk.Label(welcome_window, text="Welcome to EventSynch!", font=("Arial", 20, "bold")).pack(pady=50)

    ttk.Button(
        welcome_window, text="Get Started", command=open_login_form
    ).pack(pady=20)

    welcome_window.mainloop()

open_welcome_window()
