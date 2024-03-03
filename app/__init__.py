from flask import Flask
from .extensions import db, login_manager
from config import Config
from .routes.auth import auth
from .routes.dashboard import dashboard_bp
from .routes.api import api_bp
from .functions import Funcs
funcs = {
    'convert_timedelta': Funcs.convert_timedelta,
    'convert_float' : Funcs.convert_float,
    'convert_int':Funcs.convert_int
}
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard_bp)
    app.jinja_env.globals.update(funcs=funcs)
    return app
