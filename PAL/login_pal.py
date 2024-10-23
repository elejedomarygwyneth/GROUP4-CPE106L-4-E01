from bl.login_bl import validate_login

def login_user(username, password):
    return validate_login(username, password)
