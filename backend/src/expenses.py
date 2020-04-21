from .database.models import Expense, db


def add_expense(expense_description, expense_amount, expense_amount_paid_by, expense_shared_by, date_timestamp ):
    expense = Expense(description=expense_description,
                      amount=expense_amount,
                      paid_by=expense_amount_paid_by,
                      split_with=expense_shared_by,
                      date_time=date_timestamp)
    db.session.add(expense)


class Expenses(object):
    pass

