from sqlalchemy import and_, or_

from .database.models import UserBalance, db


def get_existing_user(expense_paid_by, expense_shared_by):
    exist_users_list = UserBalance.query.with_entities(UserBalance.id)\
        .filter(and_(or_(UserBalance.user1 == expense_paid_by, UserBalance.user2 == expense_paid_by),
                or_(UserBalance.user1 == expense_shared_by, UserBalance.user2 == expense_shared_by)))\
        .first()
    return exist_users_list


def add_to_user_balance(expense_paid_by, shared_by_user, each_person_share_amount):
    user_balance = UserBalance(user1=expense_paid_by, user2=shared_by_user, balance=each_person_share_amount)
    db.session.add(user_balance)


def update_existing_user_balance(exist_users, each_person_share_amount, expense_paid_by):
    for exist_user_id in exist_users:
        user_bal = UserBalance.query.filter(UserBalance.id == exist_user_id).one_or_none()
        if user_bal.user1 == expense_paid_by:
            user_bal.balance += each_person_share_amount
        else:
            user_bal.balance -= each_person_share_amount


def update_user_balance(expense_paid_by, expense_shared_by, each_person_share_amount):

    for shared_by_user in expense_shared_by.split(','):

        if expense_paid_by == shared_by_user.strip():
            continue

        exist_users = get_existing_user(expense_paid_by, shared_by_user.strip())

        if exist_users is None:
            add_to_user_balance(expense_paid_by, shared_by_user.strip(), each_person_share_amount)

        else:
            update_existing_user_balance(exist_users, each_person_share_amount, expense_paid_by)


class User(object):
    pass
