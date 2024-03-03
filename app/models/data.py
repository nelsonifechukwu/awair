from ..extensions import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
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
