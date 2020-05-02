from .database.models import Expense, db


def add_expense(expense_description, expense_amount, payee, list_of_receivers, date_timestamp):
    expense = Expense(description=expense_description,
                      amount=expense_amount,
                      payee=payee,
                      list_of_receivers=list_of_receivers,
                      date_time=date_timestamp
                      )
    db.session.add(expense)


class Expenses(object):
    pass

