from werkzeug.exceptions import abort
from .database.models import UserBalance, User


class UserDashboard(object):
    def __init__(self):
        pass

    def display_user_dashboard(self, user_id):
        user_name_from_model = User.query.with_entities(User.name).filter(User.id == user_id).one_or_none()

        if user_name_from_model is None:
            abort(404)

        user_name = user_name_from_model[0]
        total_user_owed_amount = 0
        total_user_lent_amount = 0
        individual_owed_details = {}
        individual_lent_details = {}

        user1_balance = UserBalance.query.filter(UserBalance.user1 == user_name).all()
        user2_balance = UserBalance.query.filter(UserBalance.user2 == user_name).all()

        for user in user1_balance:
            if user.balance < 0:
                total_user_owed_amount += user.balance
                individual_owed_details[user.user2]= user.balance

            else:
                total_user_lent_amount += user.balance
                individual_lent_details[user.user2]= user.balance

        for user in user2_balance:
            if user.balance < 0:
                user.balance *= (-1)
                total_user_lent_amount += user.balance
                individual_lent_details[user.user1] = user.balance

            else:
                total_user_owed_amount += user.balance
                individual_owed_details[user.user1] = user.balance

        return user_name, total_user_owed_amount, total_user_lent_amount, \
               individual_owed_details, individual_lent_details
