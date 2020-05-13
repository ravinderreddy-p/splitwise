from flask_login import LoginManager, current_user, login_user, logout_user

from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_cors import CORS
from .calculate_share import CalculateShare, calculate_share_per_receiver
from .config import Config
from .database.setup import setup_db, db
from .expenses import add_expense
from .forms import LoginForm
from .balance_management_service import update_all_peer_to_peer_records
from .user_management_service import UserManagement
from .user_dashboard import UserDashboard


def create_app(test_config=None):
    app = Flask(__name__)
    login = LoginManager(app)
    app.config.from_object(Config)
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
        # try:
        process_transaction(date_timestamp, description, expense_amount, list_of_receivers, payee)
        # except as e:
            # return jsonify(e)
        return jsonify({
            'success': 'true'
        })

    def process_transaction(date_timestamp, description, expense_amount, list_of_receivers, payee):
        add_expense(description, expense_amount, payee, list_of_receivers, date_timestamp)
        each_person_share_amount = calculate_share_per_receiver(expense_amount, list_of_receivers)
        update_all_peer_to_peer_records(payee, list_of_receivers, each_person_share_amount)
        db.session.commit()  # data access layer

    @app.route('/dashboard/<int:user_id>', methods=['GET'])
    def display_dashboard(user_id):
        user_id, \
        total_user_owed_amount, \
        total_user_lent_amount, \
        user_owed_to_dict, \
        user_lent_to_dict = UserDashboard().display_user_dashboard(user_id)
        return jsonify({
            'user_id': user_id,
            'total_user_lent_amount': total_user_lent_amount,
            'total_user_owed_amount': total_user_owed_amount,
            'user_lent_to_peers': user_lent_to_dict,
            'user_owed_to_peers': user_owed_to_dict
        })

    @app.route('/user', methods=['POST'])
    def add_user():
        body = request.get_json()
        user_name = UserManagement().create_a_new_user(body)
        return jsonify({
            "user": user_name,
            "success": "true"
        })

    @app.route('/index', methods=['GET'])
    @app.route('/home', methods=['GET'])
    @app.route('/')
    def home():
        user = {'username': 'Miguel'}
        return render_template('index.html')


    @app.route('/login', methods=['GET', 'POST'])
    def signin():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = login_user(form.username.data)
            if user is None or not user.check_password(form.password.data):
                flash('Invalid user name or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        return render_template('login.html', title='Sign In', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    return app
