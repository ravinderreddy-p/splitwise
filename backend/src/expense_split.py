from sqlalchemy import or_

from .database.models import User


class ExpenseSplit:
    def __init__(self):
        pass

    def convert_user_id_to_name(self):
        user_list = []
        users = User.query.with_entities(User.name) \
            .filter(or_(User.id == int(self[0]),
                        User.id == int(self[1]),
                        User.id == int(self[2]))).all()

        for user in users:
            user_list.append(user[0])

        expense_shared_by = ",".join(user_list)
        return expense_shared_by
