from flask import Blueprint
from flask_restful import Resource, reqparse
from ..extensions import db, api
from ..models.device import *
from ..models.data import *
from ..models.forecast import *
from geopy.geocoders import Nominatim
from ..exceptions import ValException
from ..openmeteo import OpenMeteoStore
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, not_

#Look for something else other than geopy !!!!!!!!!!!!!!!!!!!!!!!!! 
try:
    geolocator = Nominatim(user_agent="my-app")
except:
    print("Geolocator Timed out")

api_bp = Blueprint('api', __name__)
api.init_app(api_bp)

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
            is_float = ValException(temperature=data["temperature"], pressure=data["pressure"], humidity=data["humidity"]).check_type_float()
            if is_float:
                if devices:
                    if devices.location:
                        lat = devices.location.split(',')[0]
                        lon = devices.location.split(',')[1]
                        if devices.last_forecast:
                            if datetime.now() - devices.last_forecast > timedelta(hours=24):
                                x = OpenMeteoStore(lat, lon, str(devices.id)).store_data_rel()
                                Hourly.query.filter_by(darla_id = devices.id).delete()
                                Daily.query.filter_by(darla_id =devices.id).delete()
                                db.session.bulk_save_objects(x)
                                db.session.commit()         
                                devices.last_forecast = datetime.now()
                        else:
                            x = OpenMeteoStore(lat, lon, str(devices.id)).store_data_rel()
                            Hourly.query.filter_by(darla_id = devices.id).delete()
                            Daily.query.filter_by(darla_id =devices.id).delete()
                            db.session.bulk_save_objects(x)
                            db.session.commit()   
                            devices.last_forecast = datetime.now()
                    # all = Hourly.query.filter(and_(Hourly.date_forecast> datetime.now(), Hourly.date_forecast <= datetime.now()+timedelta(hours=24))).all()
                    # for al in all:
                    #     print(al.temperature_2m)

                    new = Data(temperature=data["temperature"], pressure=data["pressure"], humidity=data["humidity"], darla_id=uuid["uuid"])
                    db.session.add(new)
                    devices.last_updated = datetime.now()
                    db.session.commit()
                    return "Created", 201
                else:
                    return "No device",404
            else:
                return "Wrong type values passed", 403
        except Exception as e:
            return f"Forbidden: Incorrect UUID or {e}", 403
        
class WindData(Resource):
    def post(self):
        uuid = device_arg.parse_args()
        data = wind_data.parse_args()
        try:
            devices = Darla.query.filter_by(id=uuid.get("uuid")).first()
            is_float = ValException(wind_speed=data["wind-speed"], wind_direction=data["wind-direction"]).check_type_float()
            if is_float:
                if devices:
                    new = Wind(wind_speed=data["wind-speed"], wind_direction=data["wind-direction"], cloud_cover=data["cloud-cover"], darla_id=uuid["uuid"])
                    db.session.add(new)
                    devices.last_updated = datetime.now()
                    db.session.commit()
                    return "Created", 201
                else:
                    return "No device",404
            else:
                return "Wrong type values passed", 403
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
            is_float = ValException(pmtwo=data["pm2.5"], pmten=data["pm10"], co_index=data["co_index"]).check_type_float()
            if is_float:
                if devices:
                    new = AirQuality(pmtwo=data["pm2.5"], pmten=data["pm10"], co_index=data["co_index"], darla_id=uuid["uuid"])
                    db.session.add(new)
                    devices.last_updated = datetime.now()
                    db.session.commit()
                    return "Created", 201
                else:
                    return "No device",404
            else:
                return "Wrong type values passed", 403
        except:
            return "Forbidden: Incorrect UUID ", 403
        
api.add_resource(TempData,"/temp")
api.add_resource(WindData,"/wind")
api.add_resource(RainData,"/rain")
api.add_resource(LocationData,"/location")
api.add_resource(AirQualityData, "/airqo")
