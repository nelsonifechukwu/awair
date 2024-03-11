from app import create_app
from app.extensions import db
from app.models import Darla, AirQuality
from app.generateID import Generate

app = create_app()
