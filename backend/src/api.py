from sqlalchemy import and_, or_

from flask import Flask, request, jsonify
from flask_cors import CORS
from .calculate_share import CalculateShare, calculate_each_share
from .database import models
from .database.models import Expense, db, setup_db, UserBalance
from .expenses import add_expense
from .user_balance import update_user_balance


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
        body = request.get_json()
        description = body.get('description')
        paid_by = body.get('paid_by')
        expense_amount = body.get('amount')
        team = body.get('team')
        expense_shared_by = body.get('split_with')
        date_timestamp = body.get('timestamp')
        add_expense(description, expense_amount, paid_by, expense_shared_by, date_timestamp)
        each_person_share_amount = calculate_each_share(expense_amount, expense_shared_by)
        update_user_balance(paid_by, expense_shared_by, each_person_share_amount)

        db.session.commit()

        return jsonify({
            'success': 'true'
        })

    return app
