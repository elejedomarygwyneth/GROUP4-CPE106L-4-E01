import tkinter as tk
from tkinter import messagebox
from PAL.login_pal import login_user
from UI.dashboard_ui import open_dashboard

def login():
    username = entry_username.get()
    password = entry_password.get()
    if login_user(username, password):
        messagebox.showinfo("Login Success", "Welcome to the EventSynch Dashboard")
        root.destroy()  # Close login window
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

root = tk.Tk()
root.title("EventSynch Login")
root.geometry("300x200")

tk.Label(root, text="Username").pack(pady=10)
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack(pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()


