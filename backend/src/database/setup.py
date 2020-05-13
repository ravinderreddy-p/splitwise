from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

database_name = 'split_wise'
database_path = 'postgres://pravinderreddy@localhost:5432/split_wise'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate()
    db.init_app(app)
    migrate.init_app(app, db)
    # db.create_all()