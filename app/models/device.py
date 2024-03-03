from ..extensions import db
from sqlalchemy.dialects.postgresql import UUID,BOOLEAN
import uuid 
from datetime import datetime
class Darla(db.Model):
    id = db.Column(UUID(as_uuid = True), nullable=False, primary_key = True, default = uuid.uuid4)
    device_id = db.Column(db.String(10), nullable=False, unique=True)
    active = db.Column(BOOLEAN, nullable = False, default=0)
    date = db.Column(db.DateTime, nullable = False, default = datetime.now)
    last_updated = db.Column(db.DateTime)
    last_forecast = db.Column(db.DateTime)
    place = db.Column(db.String(100))
    location = db.Column(db.String(50))
    battery = db.Column(db.String(10))
    signal = db.Column(db.String(10))
    data = db.relationship('Data', backref=db.backref('Data'))
    wind = db.relationship('Wind', backref=db.backref('Wind'))
    rain = db.relationship('Rain', backref=db.backref('Rain'))
    airquality = db.relationship('AirQuality', backref=db.backref('AirQuality'))
    hourly = db.relationship('Hourly', backref=db.backref('Hourly'))
