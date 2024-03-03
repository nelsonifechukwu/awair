from ..extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
class Hourly(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key = True)
    darla_id = db.Column(UUID(as_uuid = True), db.ForeignKey('darla.id'))
    temperature_2m = db.Column(db.String(50))
    relative_humidity_2m = db.Column(db.String(50))
    apparent_temperature = db.Column(db.String(50))
    rain = db.Column(db.String(50))
    surface_pressure = db.Column(db.String(50))
    wind_speed_10m = db.Column(db.String(50))
    wind_direction_10m = db.Column(db.String(50))
    date_forecast = db.Column(db.DateTime)

class Daily(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key = True)
    darla_id = db.Column(UUID(as_uuid = True), db.ForeignKey('darla.id'))
    temperature_2m_min = db.Column(db.String(50))
    temperature_2m_max = db.Column(db.String(50))
    date_forecast = db.Column(db.DateTime)

