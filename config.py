import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
class Config:
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASS = os.environ.get('POSTGRES_PASS')
    POSTGRES_URL = os.environ.get('POSTGRES_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    UPLOADS = "app/static/uploads/"
    EXTS = set(['png', 'jpg', 'jpeg'])
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_URL}"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
   
    # SQLALCHEMY_DATABASE_URI ="sqlite:///test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

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
class ProductionConfig:
    pass