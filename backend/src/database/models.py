from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String, Date, DateTime

database_name = 'split_wise'
database_path = 'XYZ'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Expenses
'''
class Expense(db.Model):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Integer)
    paid_by = Column(String)
    split_with = Column(String)
    date_time = Column(DateTime)

    def __init__(self, description, amount, paid_by, split_with, date_time):
        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.split_with = split_with
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
            'paid_by': self.paid_by,
            'split_with': self.split_with,
            'date_time': self.date_time
        }


class UserBalance(db.Model):
    __tablename__= 'userbalance'
    user1 = Column(String)
    user2 = Column(String)
    balance = Column(Integer)

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