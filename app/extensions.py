from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
db = SQLAlchemy()
api = Api()
login_manager = LoginManager()


