import decimal

from sqlalchemy import and_, or_

from .database.models import UserBalance, db


def update_all_peer_to_peer_records(payee, list_of_receivers, each_person_share_amount):
    for a_receiver in list_of_receivers:
        if this_receiver_is_payee(payee, a_receiver):
            continue
        peer_to_peer_balance_record = get_peer_to_peer_balance_record(payee, a_receiver)
        if no_previous_relationship_between_payee_and_user(peer_to_peer_balance_record):
            peer_to_peer_balance_record = create_peer_to_peer_balance_record(
                                            user_1=payee,
                                            user_2=a_receiver,
                                            balance=each_person_share_amount
                                            )
        else:
            update_peer_to_peer_balance_record(peer_to_peer_balance_record, each_person_share_amount, payee)
        db.session.add(peer_to_peer_balance_record)


def get_list_of_receivers(comma_seperated_list_of_receivers):
    return comma_seperated_list_of_receivers.split(',')


def update_peer_to_peer_balance_record(peer_to_peer_balance, each_person_share_amount, payee):
    if user_is_payee(user=peer_to_peer_balance.user1, payee=payee):
        add_to_balance(each_person_share_amount, peer_to_peer_balance)
    else:
        subtract_from_balance(each_person_share_amount, peer_to_peer_balance)


def create_peer_to_peer_balance_record(user_1, user_2, balance):
    user_balance = UserBalance(user1=user_1, user2=user_2, balance=balance)
    return user_balance


def get_peer_to_peer_balance_record(payee, receiver):
    peer_to_peer_balance_record = UserBalance.query\
        .filter(and_(or_(UserBalance.user1 == payee, UserBalance.user2 == payee),
                     or_(UserBalance.user1 == receiver, UserBalance.user2 == receiver)))\
        .first()
    return peer_to_peer_balance_record


def user_is_payee(user, payee):
    return user == payee


def subtract_from_balance(amount, peer_to_peer_balance):
    peer_to_peer_balance.balance -= decimal.Decimal(amount)


def add_to_balance(amount, peer_to_peer_balance):
    peer_to_peer_balance.balance += amount


def this_receiver_is_payee(payee, a_user):
    return payee == a_user


def no_previous_relationship_between_payee_and_user(peer_to_peer_balance):
    return peer_to_peer_balance is None