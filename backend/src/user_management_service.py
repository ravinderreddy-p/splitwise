from .database.models import User, db


class UserManagement(object):
    def __init__(self):
        pass


    def create_a_new_user(self, request_body):
        user_name = request_body.get('user_name')
        email_id = request_body.get('email_id')
        password = request_body.get('password')
        user = User(name=user_name, email_id=email_id)
        user.set_password(password=password)
        db.session.add(user)
        db.session.commit()
        return user_name


    def get_login_user(self, user_name):
        login_user = User.query.filter_by(name=user_name).first()
        return login_user