from flask_restful import Resource, reqparse, fields, marshal_with, abort,request
from .extensions import db, api
from .models import *
from geopy.geocoders import Nominatim
try:
    geolocator = Nominatim(user_agent="my-app")
except:
    print("Geolocator Timed out")

# API (Device)
device_arg = reqparse.RequestParser()
temp_data = reqparse.RequestParser()
wind_data = reqparse.RequestParser()
rain_data = reqparse.RequestParser()
location_data = reqparse.RequestParser()
airquality_data = reqparse.RequestParser()
device_arg.add_argument("uuid", type=str, help='UUID of device', required=True)
temp_data.add_argument("pressure", type=str, help='This is required', required=True)
temp_data.add_argument("temperature", type=str, help='This is required', required=True)
temp_data.add_argument("humidity", type=str,  help='This is required', required=True)
wind_data.add_argument("wind-speed", type=str,  help='This is required', required=True)
wind_data.add_argument("wind-direction", type=str,  help='This is required', required=True)
wind_data.add_argument("cloud-cover", type=str,  help='This is required', default="none")
rain_data.add_argument("rain", type=str, help='This is required', required=True)
airquality_data.add_argument("pm2.5", type=str, help='This is required', required=True)
airquality_data.add_argument("pm10", type=str, help='This is required', required=True)
airquality_data.add_argument("co_index", type=str, help='This is required', required=True)
location_data.add_argument("location", type=str, help='This is required', required=True)
location_data.add_argument("battery", type=str, help='This is required', required=True)
location_data.add_argument("signal", type=str, help='This is required', required=True)



class TempData(Resource):
    def post(self):
        uuid = device_arg.parse_args()
        data = temp_data.parse_args()
        try:
            devices = Darla.query.filter_by(id=uuid.get("uuid")).first()
            if devices:
                new = Data(temperature=data["temperature"], pressure=data["pressure"], humidity=data["humidity"], darla_id=uuid["uuid"])
                db.session.add(new)
                devices.last_updated = datetime.now()
                db.session.commit()
                return "Created", 201
            else:
                return "No device",404
        except:
            return "Forbidden: Incorrect UUID ", 403
        
class WindData(Resource):
    def post(self):
        uuid = device_arg.parse_args()
        data = wind_data.parse_args()
        try:
            devices = Darla.query.filter_by(id=uuid.get("uuid")).first()
            if devices:
                new = Wind(wind_speed=data["wind-speed"], wind_direction=data["wind-direction"], cloud_cover=data["cloud-cover"], darla_id=uuid["uuid"])
                db.session.add(new)
                devices.last_updated = datetime.now()
                db.session.commit()
                return "Created", 201
            else:
                return "No device",404
        except:
            return "Forbidden: Incorrect UUID ", 403

class RainData(Resource):
    def post(self):
        uuid = device_arg.parse_args()
        data = rain_data.parse_args()
        try:
            devices = Darla.query.filter_by(id=uuid.get("uuid")).first()
            if devices:
                new = Rain(rain=data["rain"], darla_id=uuid["uuid"])
                db.session.add(new)
                devices.last_updated = datetime.now()
                db.session.commit()
                return "Created", 201
            else:
                return "No device",404
        except:
            return "Forbidden: Incorrect UUID ", 403

# change location because of new data points to be added.
class LocationData(Resource):
    def post(self):
        uuid = device_arg.parse_args()
        data = location_data.parse_args()
        place = geolocator.reverse(data["location"])
        place = place.address.split(",")[0]
        print(place)
        try:
            devices = Darla.query.filter_by(id=uuid.get("uuid")).first()
            if devices:
                try:
                    place = geolocator.reverse(data["location"])
                    place = place.address.split(",")[0]
                except:
                    print("Geopy timed out !!!!!")
                devices.location = data['location']
                devices.battery = data['battery']
                devices.signal = data['signal']
                devices.last_updated = datetime.now()
                devices.place = place
                db.session.commit()
                return "Created", 201
            else:
                return "No device",404
        except Exception as e:
            print(e)
            return "Forbidden: Incorrect UUID ", 403

class AirQualityData(Resource):
    def post(self):
        uuid = device_arg.parse_args()
        data = airquality_data.parse_args()
        try:
            devices = Darla.query.filter_by(id=uuid.get("uuid")).first()
            if devices:
                new = AirQuality(pmtwo=data["pm2.5"], pmten=data["pm10"], co_index=data["co_index"], darla_id=uuid["uuid"])
                db.session.add(new)
                devices.last_updated = datetime.now()
                db.session.commit()
                return "Created", 201
            else:
                return "No device",404
        except:
            return "Forbidden: Incorrect UUID ", 403
        

# RESOURCE FIELDS FOR GET REQUEST RETURN 
# resource_fields = {
#     "uuid":fields.String,
#     "pressure":fields.String,
#     "temperature":fields.String,
#     "humidity":fields.String,
#     "wind-speed":fields.String,
#     "wind-direction":fields.String,
#     "rain":fields.String,
#     "pm2.5":fields.String,
#     "pm10":fields.String,
#     "co_index":fields.String,
#     "cloud-cover":fields.String,
#     "location":fields.String,
# }
# tempData_fields = {
#     "uuid":fields.String,
#     "pressure":fields.String,
#     "temperature":fields.String,
#     "humidity":fields.String,
# }
# windData_fields = {
#     "uuid":fields.String,
#     "wind-speed":fields.String,
#     "wind-direction":fields.String,
#     "cloud-cover":fields.String,
# }
# airq_fields = {
#     "uuid":fields.String,
#     "pm2.5":fields.String,
#     "pm10":fields.String,
#     "co_index":fields.String,
# }
# rain_fields = {
#     "uuid":fields.String,
#     "rain":fields.String,
# }
# location_fields = {
#     "uuid":fields.String,
#     "location":fields.String,
# }