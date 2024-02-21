from .extensions import db, UserMixin
from sqlalchemy.dialects.postgresql import UUID,BOOLEAN
import uuid 
from datetime import datetime

# Add name to Darla !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Darla(db.Model):
    id = db.Column(UUID(as_uuid = True), nullable=False, primary_key = True, default = uuid.uuid4)
    device_id = db.Column(db.String(10), nullable=False, unique=True)
    active = db.Column(BOOLEAN, nullable = False, default=0)
    date = db.Column(db.DateTime, nullable = False, default = datetime.now)
    last_updated = db.Column(db.DateTime)
    place = db.Column(db.String(100))
    location = db.Column(db.String(50))
    battery = db.Column(db.String(10))
    signal = db.Column(db.String(10))
    data = db.relationship('Data', backref=db.backref('Data'))
    wind = db.relationship('Wind', backref=db.backref('Wind'))
    rain = db.relationship('Rain', backref=db.backref('Rain'))
    airquality = db.relationship('AirQuality', backref=db.backref('AirQuality'))

class Data(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    darla_id = db.Column(UUID(as_uuid = True), db.ForeignKey('darla.id'))
    pressure = db.Column(db.String(10), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    humidity = db.Column(db.String(10), nullable=False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.now)

class Wind(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    darla_id = db.Column(UUID(as_uuid = True), db.ForeignKey('darla.id'))
    wind_speed = db.Column(db.String(10), nullable=False)
    wind_direction = db.Column(db.String(10), nullable=False)
    cloud_cover = db.Column(db.String(10), nullable=False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.now)
class Rain(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    darla_id = db.Column(UUID(as_uuid = True), db.ForeignKey('darla.id')) 
    rain = db.Column(db.String(10), nullable=False)   
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.now)
class AirQuality(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    darla_id = db.Column(UUID(as_uuid = True), db.ForeignKey('darla.id')) 
    pmtwo = db.Column(db.String(10), nullable=False)
    pmten = db.Column(db.String(10), nullable=False)
    co_index = db.Column(db.String(10), nullable=False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.now)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key = True)
    username = db.Column(db.String(30), nullable=False, unique = True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    key = db.Column(db.String(120), nullable=False)
    # add profile picture (Optional) more than 20 for google sign in !!!!!!!!!!!!!!!!!!!!!!
    profile_picture = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.now)
    uuid = db.relationship('Uuid', backref=db.backref('Uuid'))

class Uuid(db.Model):
    uuid_id = db.Column(db.Integer, nullable=False, primary_key=True)
    uuid = db.Column(UUID(as_uuid = True), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.now)
    



