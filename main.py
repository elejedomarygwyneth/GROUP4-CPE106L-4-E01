from ui import login_ui
from data import db_connection

if __name__ == "__main__":
    db_connection.create_tables()  # Initialize the database
    # Start the login UI
    login_ui.root.mainloop()

