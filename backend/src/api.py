from flask import Flask, request, jsonify
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    # setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,True')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Hello World'

    @app.route('/transaction/<int:user_id>', methods=['POST'])
    def add_transaction(user_id):
        body = request.get_json()
        description = body.get('description')
        paid_by = body.get('paid_by')
        amount = body.get('amount')
        team = body.get('team')
        split_with = body.get('split_with')
        date_timestamp = body.get('timestamp')

        return jsonify({
            'success': 'true'
        })

    return app

