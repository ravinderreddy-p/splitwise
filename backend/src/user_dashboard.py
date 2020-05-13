from sqlalchemy import or_
from werkzeug.exceptions import abort
from .database.models import UserBalance, User


class UserDashboard(object):
    def __init__(self):
        pass


    def display_user_dashboard(self, user_id):
        total_user_owed_amount = 0
        total_user_lent_amount = 0
        user_owed_details_dict = {}
        user_lent_details_dict = {}
        peer_to_peer_balance_records = self.get_peer_to_peer_balance_records(user_id)
        for a_peer_to_peer_balance_record in peer_to_peer_balance_records:
            total_user_lent_amount, total_user_owed_amount = self.process_each_record(a_peer_to_peer_balance_record,
                                                                                      total_user_lent_amount,
                                                                                      total_user_owed_amount, user_id,
                                                                                      user_lent_details_dict,
                                                                                      user_owed_details_dict)
        return user_id, total_user_owed_amount, total_user_lent_amount, \
               user_owed_details_dict, user_lent_details_dict

    def process_each_record(self, a_peer_to_peer_balance_record, total_user_lent_amount, total_user_owed_amount,
                            user_id, user_lent_details_dict, user_owed_details_dict):
        if self.user_is_peer_1(user_id, a_peer_to_peer_balance_record.user1):
            total_user_lent_amount, total_user_owed_amount = self.process_a(a_peer_to_peer_balance_record,
                                                                            total_user_lent_amount,
                                                                            total_user_owed_amount,
                                                                            user_lent_details_dict,
                                                                            user_owed_details_dict)
        else:
            total_user_lent_amount, total_user_owed_amount = self.process_b(a_peer_to_peer_balance_record,
                                                                            total_user_lent_amount,
                                                                            total_user_owed_amount,
                                                                            user_lent_details_dict,
                                                                            user_owed_details_dict)
        return total_user_lent_amount, total_user_owed_amount

    def process_b(self, a_peer_to_peer_balance_record, total_user_lent_amount, total_user_owed_amount,
                  user_lent_details_dict, user_owed_details_dict):
        if not self.user_owed_to_other_peer(a_peer_to_peer_balance_record.balance):
            total_user_owed_amount = self.calculate_peer_to_peer_balance_amount(a_peer_to_peer_balance_record,
                                                                                user_owed_details_dict,
                                                                                total_user_owed_amount,
                                                                                a_peer_to_peer_balance_record.user1)
        else:
            self.multiply_balance_with_negetive_one(a_peer_to_peer_balance_record)
            total_user_lent_amount = self.calculate_peer_to_peer_balance_amount(a_peer_to_peer_balance_record,
                                                                                user_lent_details_dict,
                                                                                total_user_lent_amount,
                                                                                a_peer_to_peer_balance_record.user1)
        return total_user_lent_amount, total_user_owed_amount

    def process_a(self, a_peer_to_peer_balance_record, total_user_lent_amount, total_user_owed_amount,
                  user_lent_details_dict, user_owed_details_dict):
        if self.user_owed_to_other_peer(a_peer_to_peer_balance_record.balance):
            self.multiply_balance_with_negetive_one(a_peer_to_peer_balance_record)
            total_user_owed_amount = self.calculate_peer_to_peer_balance_amount(a_peer_to_peer_balance_record,
                                                                                user_owed_details_dict,
                                                                                total_user_owed_amount,
                                                                                a_peer_to_peer_balance_record.user2)
        else:
            total_user_lent_amount = self.calculate_peer_to_peer_balance_amount(a_peer_to_peer_balance_record,
                                                                                user_lent_details_dict,
                                                                                total_user_lent_amount,
                                                                                a_peer_to_peer_balance_record.user2)
        return total_user_lent_amount, total_user_owed_amount

    def multiply_balance_with_negetive_one(self, a_balance_record):
        a_balance_record.balance *= (-1)


    def calculate_peer_to_peer_balance_amount(self, peer_to_peer_balance_record, peer_balance,
                                              total_user_to_peer_amount, peer):
        total_user_to_peer_amount += peer_to_peer_balance_record.balance
        peer_balance[peer] = peer_to_peer_balance_record.balance
        return total_user_to_peer_amount


    def get_peer_to_peer_balance_records(self, user_id):
        return UserBalance.query.filter(or_(UserBalance.user1 == user_id, UserBalance.user2 == user_id)).all()


    def user_owed_to_other_peer(self, balance):
        return balance < 0


    def user_is_peer_1(self, user, peer):
        return user == peer
