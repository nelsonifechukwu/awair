from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_caching import Cache
db = SQLAlchemy()
api = Api()
login_manager = LoginManager()
migrate = Migrate()
cache = Cache()