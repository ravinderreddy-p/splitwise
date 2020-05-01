from sqlalchemy import and_, or_
import simplejson as json

from flask import Flask, request, jsonify
from flask_cors import CORS
from .calculate_share import CalculateShare, calculate_share_per_receiver
from .database import models
from .database.models import Expense, db, setup_db, UserBalance, User
from .expenses import add_expense
from .peer_to_peer_balance import update_all_peer_to_peer_records
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

    @app.route('/health_check')
    def index():
        return 'I am healthy'

    @app.route('/transaction', methods=['POST'])
    def add_transaction():
        body = request.get_json()
        description = body.get('description')
        payee = body.get('payee')
        expense_amount = body.get('amount')
        list_of_receivers = body.get('list_of_receivers')
        date_timestamp = body.get('timestamp')
        add_expense(description, expense_amount, payee, list_of_receivers, date_timestamp)
        each_person_share_amount = calculate_share_per_receiver(expense_amount, list_of_receivers)
        update_all_peer_to_peer_records(payee, list_of_receivers, each_person_share_amount)
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
