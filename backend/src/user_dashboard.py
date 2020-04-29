from .database.models import UserBalance


class UserDashboard(object):
    def __init__(self):
        pass

    def display_user_dashboard(self):
        user_owed = 0
        user_lent = 0
        user_owed_to = {}
        user_lent_to = {}

        user1_balance = UserBalance.query.filter(UserBalance.user1 == 'Ravi').all()
        user2_balance = UserBalance.query.filter(UserBalance.user2 == 'Ravi').all()
        for user in user1_balance:
            if user.balance < 0:
                user_owed += user.balance
                user_owed_to[user.user2]: user.balance

            else:
                user_lent += user.balance
                user_lent_to[user.user2]: user.balance

        for user in user2_balance:
            if user.balance < 0:
                user.balance *= (-1)
                user_lent += user.balance
                user_lent_to[user.user1] = user.balance

            else:
                user_owed += user.balance
                user_owed_to[user.user1] = user.balance

        return user_owed, user_lent, user_owed_to, user_lent_to
