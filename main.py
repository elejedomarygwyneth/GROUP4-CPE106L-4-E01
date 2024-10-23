from UI import login_ui
from DATABASE import db_connection

if __name__ == "__main__":
    db_connection.create_tables()  # Initialize the database
    # Start the login UI
    login_ui.root.mainloop()

