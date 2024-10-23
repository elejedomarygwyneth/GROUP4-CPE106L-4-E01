from flask import Flask
from config import Config
from dal.dal import db
from ui.login_ui import setup_login_routes
from ui.dashboard_ui import setup_dashboard_routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

setup_login_routes(app)
setup_dashboard_routes(app)

if __name__ == '__main__':
    app.run(debug=True)

