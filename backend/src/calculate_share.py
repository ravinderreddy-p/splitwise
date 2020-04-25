def calculate_each_share(expense_amount, expense_shared_by):
    number_of_users = len(expense_shared_by.split(','))
    each_share_amount = float(expense_amount) / number_of_users
    return each_share_amount


class CalculateShare:
    pass
