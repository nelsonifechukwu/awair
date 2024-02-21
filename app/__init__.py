from flask import Flask
from .extensions import db, api, login_manager
from config import Config
from .routes import main, convert_timedelta, convert_int
funcs = {
    'convert_timedelta': convert_timedelta,
    'convert_int' : convert_int
}
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    api.init_app(app)  
    login_manager.init_app(app)
    app.register_blueprint(main)
    app.jinja_env.globals.update(funcs=funcs)
    return app
