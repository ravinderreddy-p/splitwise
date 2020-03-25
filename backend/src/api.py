from flask import Flask, request
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

    @app.route('/transaction/<int:user_id>', methods=['POST'])
    def add_transaction(user_id):
        body = request.get_json()

