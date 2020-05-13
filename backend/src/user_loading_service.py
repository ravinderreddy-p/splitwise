from backend.src.api import create_app
from backend.src.database.models import User


@create_app.login.user_loader
def load_user(id):
    return User.query.get(int(id))
