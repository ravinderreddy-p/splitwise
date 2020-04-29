from sqlalchemy import and_, or_
import simplejson as json

from flask import Flask, request, jsonify
from flask_cors import CORS
from .calculate_share import CalculateShare, calculate_each_share
from .database import models
from .database.models import Expense, db, setup_db, UserBalance, User
from .expenses import add_expense
from .user_balance import UsersBalanceUpdate
from .expense_split import ExpenseSplit
from .add_new_user import AddNewUser
from .user_dashboard import UserDashboard


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,True')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Hello World'

    @app.route('/transaction', methods=['POST'])
    def add_transaction():
        user_list = []
        body = request.get_json()
        description = body.get('description')
        paid_by = body.get('paid_by')
        expense_amount = body.get('amount')
        expense_split_by = body.get('split_by').split(',')
        date_timestamp = body.get('timestamp')

        expense_shared_by = ExpenseSplit.convert_user_id_to_name(expense_split_by)

        add_expense(description, expense_amount, paid_by, expense_shared_by, date_timestamp)

        each_person_share_amount = calculate_each_share(expense_amount, expense_shared_by)

        UsersBalanceUpdate.update_user_balance(paid_by.strip(), expense_shared_by, each_person_share_amount)

        db.session.commit()

        return jsonify({
            'success': 'true'
        })

    @app.route('/dashboard/<int:user_id>', methods=['GET'])
    def display_dashboard(user_id):
        user_name, \
        total_user_owed_amount, \
        total_user_lent_amount, \
        individual_owed_details, \
        individual_lent_details = UserDashboard().display_user_dashboard(user_id)

        return jsonify({
            'user': user_name,
            'user_lent': total_user_lent_amount,
            'user_owed': total_user_owed_amount,
            'user_lent_to': individual_lent_details,
            'user_owed_to': individual_owed_details

        })

    @app.route('/user', methods=['POST'])
    def add_user():
        body = request.get_json()
        user_name = AddNewUser().add_new_user(body)

        return jsonify({
            "user": user_name,
            "success": "true"
        })

    return app
