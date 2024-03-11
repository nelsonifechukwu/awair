from app import create_app
from app.extensions import db
from app.models.device import Darla 
from app.models.data import AirQuality
from app.generateID import Generate

app = create_app()

