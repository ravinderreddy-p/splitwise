from .database.models import User, db


class AddNewUser(object):
    def __init__(self):
        pass

    def add_new_user(self):
        user_name = self.get('user_name')
        user = User(name=user_name)
        db.session.add(user)
        db.session.commit()
        return user_name
