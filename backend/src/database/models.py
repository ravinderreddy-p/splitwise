from backend.src.database.setup import db
from flask_login import UserMixin
from sqlalchemy import Integer, Column, String, Date, DateTime, Float
from werkzeug.security import generate_password_hash, check_password_hash
# from backend.src.api import login

'''
Expenses
'''


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
    payee = Column(Integer)
    list_of_receivers = Column(db.ARRAY(db.Integer()))
    date_time = Column(DateTime)

    def __init__(self, description, amount, payee, list_of_receivers, date_time):
        self.description = description
        self.amount = amount
        self.payee = payee
        self.list_of_receivers = list_of_receivers
        self.date_time = date_time

    def insert(self):
        db.session.add()
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'paid_by': self.payee,
            'split_with': self.list_of_receivers,
            'date_time': self.date_time
        }


'''
UserBalance
'''


class UserBalance(db.Model):
    __tablename__ = 'userbalance'
    id = Column(Integer, primary_key=True)
    user1 = Column(Integer)
    user2 = Column(Integer)
    balance = Column(db.Numeric(10, 2))

    def __init__(self, user1, user2, balance):
        self.user1 = user1
        self.user2 = user2
        self.balance = balance

    def insert(self):
        db.session.add()
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'user1': self.user1,
            'user2': self.user2,
            'balance': self.balance
        }


'''
User
'''
# @login.user_loader
# def load_user(user_id):
#     return User.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email_id = Column(String)
    password_hash = Column(String)

    def __init__(self, name, email_id):
        self.name = name
        self.email_id = email_id
        # self.password_hash = password_hash

    def insert(self):
        db.session.add()
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'user': self.name,
            'email_id': self.email_id,
            'password_hash': self.password_hash
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
