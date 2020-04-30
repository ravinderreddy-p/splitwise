from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String, Date, DateTime, Float
from flask_migrate import Migrate

database_name = 'split_wise'
database_path = 'postgres://pravinderreddy@localhost:5432/split_wise'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate()
    db.init_app(app)
    migrate.init_app(app, db)
    # db.create_all()


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


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add()
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'user': self.name
        }
