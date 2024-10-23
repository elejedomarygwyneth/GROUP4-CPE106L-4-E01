from flask import render_template, session, redirect, url_for

def setup_dashboard_routes(app):
    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('login'))
        return render_template('dashboard.html', username=session['username'])
