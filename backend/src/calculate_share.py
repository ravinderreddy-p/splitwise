def calculate_each_share(expense_amount, expense_shared_by):
    each_share_amount = float(expense_amount) / len(expense_shared_by.split(','))
    return each_share_amount


class CalculateShare:
    pass
