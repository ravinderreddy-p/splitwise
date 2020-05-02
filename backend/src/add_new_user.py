from .database.models import User, db


class AddNewUser(object):
    def __init__(self):
        pass

    def create_a_new_user(self, request_body):
        user_name = request_body.get('user_name')
        email_id = request_body.get('email_id')
        user = User(name=user_name, email_id=email_id)
        db.session.add(user)
        db.session.commit()
        return user_name
