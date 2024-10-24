import tkinter as tk
from tkinter import ttk, messagebox
from PAL.login_pal import login_user
from UI.dashboard_ui import open_dashboard

def login():
    """Handles user login."""
    username = entry_username.get()
    password = entry_password.get()
    
    if login_user(username, password):
        messagebox.showinfo("Login Success", "Welcome to the EventSynch Dashboard")
        root.destroy()  
        open_dashboard()  
    else:
        messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

root = tk.Tk()
root.title("EventSynch Login")
root.geometry("400x300")
root.configure(bg="#d4ebf2")

style = ttk.Style()
style.configure("TButton", font=("Arial", 14), padding=10)
style.configure("TLabel", background="#d4ebf2", font=("Arial", 12))

ttk.Label(root, text="EventSynch Login", font=("Arial", 18, "bold")).pack(pady=20)

ttk.Label(root, text="Username").pack(pady=5)
entry_username = ttk.Entry(root, width=30, font=("Arial", 12))
entry_username.pack(pady=5)

ttk.Label(root, text="Password").pack(pady=5)
entry_password = ttk.Entry(root, width=30, show="*", font=("Arial", 12))
entry_password.pack(pady=5)

ttk.Button(root, text="Login", command=login, style="TButton").pack(pady=20)

root.mainloop()
