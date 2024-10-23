from werkzeug.security import check_password_hash
from dal.dal import User

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return True
    return False
