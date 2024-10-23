from flask import render_template, session, redirect, url_for
from bl.event_manager import create_event, get_user_events

def setup_dashboard_routes(app):
    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('login'))
        events = get_user_events(session['user_id'])
        return render_template('dashboard.html', events=events)

    @app.route('/add_event', methods=['POST'])
    def add_event():
        # Logic for adding a new event
        pass
