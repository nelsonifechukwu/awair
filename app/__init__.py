from flask import Flask
from .extensions import db, login_manager, migrate
from config import Config
from .routes.auth import auth
from .routes.dashboard import dashboard_bp
from .routes.analytics import analytics_bp
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
    migrate.init_app(app, db)
    login_manager.init_app(app)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analytics_bp)
    app.jinja_env.globals.update(funcs=funcs)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    return app
