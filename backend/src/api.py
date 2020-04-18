from flask import Flask, request, jsonify
from flask_cors import CORS
from .database import models
from .database.models import Expense, db, setup_db, UserBalance


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
        amount = body.get('amount')
        team = body.get('team')
        split_with = body.get('split_with')
        date_timestamp = body.get('timestamp')

        no_users = len(split_with.split(','))
        split_amt_each = int(amount)/no_users

        expense = Expense(description=description,
                          amount=amount,
                          paid_by=paid_by,
                          split_with=split_with,
                          date_time=date_timestamp)

        db.session.add(expense)

        for user in split_with.split(','):
            if paid_by == user:
                continue

            user_balance = UserBalance(user1=paid_by, user2=user, balance=split_amt_each)
            db.session.add(user_balance)

        db.session.commit()
        return jsonify({
            'success': 'true'
        })

    return app
