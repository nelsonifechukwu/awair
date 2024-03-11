import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_HOST = "localhost"
    MONGO_PORT = "22743"
    MONGO_DB = "localhost:africo"
    MONGO_COL = "localhost"
    # PERMANENT_SESSION_LIFETIME = timedelta(seconds=5)
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    UPLOADS = "app/static/uploads/"
    EXTS = set(['png', 'jpg', 'jpeg'])
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_URL}"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # f"postgresql://awairdb_user:ijtmBBK6blj2uYWk8X0reivkvJqkLWjq@dpg-cnkugen79t8c73ebr1sg-a.oregon-postgres.render.com/awairdb"
    # SQLALCHEMY_DATABASE_URI ="sqlite:///test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
    MONGO_DATABASE_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

# print(Config.MONGO_DATABASE_URL)
class TestConfig:
    POSTGRES_TESTUSER = os.environ.get('POSTGRES_TESTUSER')
    POSTGRES_TESTPASS = os.environ.get('POSTGRES_TESTPASS')
    POSTGRES_TESTURL = os.environ.get('POSTGRES_TESTURL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_TESTUSER}:{POSTGRES_TESTPASS}@{POSTGRES_TESTURL}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)