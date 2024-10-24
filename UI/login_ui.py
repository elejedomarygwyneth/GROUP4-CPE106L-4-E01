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
        root.destroy()  # Close the login window
        open_dashboard()  # Open the dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

# Initialize the Tkinter window
root = tk.Tk()
root.title("EventSynch Login")
root.geometry("400x300")
root.configure(bg="#d4ebf2")

# Create a style object for modern UI
style = ttk.Style()
style.theme_use("clam")  # Use a modern theme

style.configure("TButton", font=("Arial", 12), padding=6, relief="flat", background="#4CAF50", foreground="white")
style.configure("TLabel", font=("Arial", 12), background="#d4ebf2")
style.map("TButton", background=[("active", "#45a049")])

# Username Label and Entry
ttk.Label(root, text="Admin Username").pack(pady=10)
entry_username = ttk.Entry(root, font=("Arial", 12))
entry_username.pack(pady=5)

# Password Label and Entry
ttk.Label(root, text="Admin Password").pack(pady=10)
entry_password = ttk.Entry(root, show="*", font=("Arial", 12))
entry_password.pack(pady=5)

# Login Button
ttk.Button(root, text="Login", command=login).pack(pady=20)

# Back Button (optional)
ttk.Button(root, text="Back", command=root.quit).pack()

# Start the Tkinter event loop
root.mainloop()



