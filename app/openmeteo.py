import openmeteo_requests
import json
import pickle

import requests_cache
import pandas as pd
from retry_requests import retry
import pymongo
from config import Config
from datetime import datetime, timedelta
import pandas as pd
from .models.forecast import Hourly, Daily
# Api or SDK (Not sure yet)
# API
# To store data

class OpenMeteoStore:
    def __init__(self,lat,lon, device_id, url = "https://api.open-meteo.com/v1/forecast"):
        self._lat = lat
        self._lon = lon
        self._device = device_id
        self._url = url
        self._client = client  
        self._params = self._create_param()
    def _create_param(self):
        return {
                    "latitude": self._lat,
                    "longitude": self._lon,
                    "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "rain", "surface_pressure", "wind_speed_10m", "wind_direction_10m"],
                    "daily": ["temperature_2m_max", "temperature_2m_min"],
                    "timezone": "auto",
                    # "forecast_days": 3
                }
        
    def _api_req(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session) 
        responses = openmeteo.weather_api(self._url, params=self._params)
        return responses[0]
    def convert_to_dict(self, dump):
        return {"_id": self._device, 
                "class": dump, 
                "date": datetime.now()}

   
    def store_data_rel(self): 
        response = self._api_req()
        # Hourly
        hourly = response.Hourly()
        hourly_date =  pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s"),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=hourly.Interval())
    ).to_pydatetime().tolist()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy().tolist()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy().tolist()
        hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy().tolist()
        hourly_rain = hourly.Variables(3).ValuesAsNumpy().tolist()
        hourly_surface_pressure = hourly.Variables(4).ValuesAsNumpy().tolist()
        hourly_wind_speed_10m = hourly.Variables(5).ValuesAsNumpy().tolist()
        hourly_wind_direction_10m = hourly.Variables(6).ValuesAsNumpy().tolist()
        hourly_list = [Hourly(darla_id =self._device, temperature_2m=val1, relative_humidity_2m=val2, apparent_temperature=val3, rain=val4, surface_pressure=val5, wind_speed_10m=val6, wind_direction_10m=val7, date_forecast = val8) for val1, val2, val3, val4, val5, val6 , val7, val8 in zip(hourly_temperature_2m, hourly_relative_humidity_2m, hourly_apparent_temperature, hourly_rain, hourly_surface_pressure, hourly_wind_speed_10m, hourly_wind_direction_10m, hourly_date)]
        # Daily 
        daily = response.Daily()
        daily_date =  pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s"),
        end=pd.to_datetime(daily.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=daily.Interval())
    ).to_pydatetime().tolist()
        temperature_2m_max = daily.Variables(0).ValuesAsNumpy().tolist()
        temperature_2m_min = daily.Variables(1).ValuesAsNumpy().tolist()
        daily_list = [Daily(darla_id =self._device, temperature_2m_max= val1, temperature_2m_min = val2, date_forecast = val3) for val1, val2, val3 in zip(temperature_2m_max, temperature_2m_min, daily_date)]
        instances = hourly_list + daily_list
        return instances
    
    


# No longer USEFUL 
# # To view data
# class OpenMeteoView(OpenMeteoStore):
#     def __init__(self, lat, lon, device_id, url="https://api.open-meteo.com/v1/forecast",client = pymongo.MongoClient(Config.MONGO_DATABASE_URL)[Config.MONGO_DB][Config.MONGO_COL]):
#         super().__init__(lat, lon, device_id, url, client)
#         self._class = self._load_class()
#         self._hourly_return = self._json_hourly()
#         self._daily_return =self._json_daily()

#     def _load_class(self):
#         for x in self._client.find({'_id':self._device}):
#             y = x
#         data = pickle.loads(y['class'])
#         return data

#     def _json_hourly(self):
#         hourly_json_data = {}
#         hourly = self._class.Hourly()
#         hourly_json_data["date"] =  pd.date_range(
#         start=pd.to_datetime(hourly.Time(), unit="s"),
#         end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
#         freq=pd.Timedelta(seconds=hourly.Interval())
#     ).to_pydatetime().tolist()
#         hourly_json_data['hourly_temperature_2m'] = hourly.Variables(0).ValuesAsNumpy().tolist()
#         hourly_json_data['hourly_relative_humidity_2m'] = hourly.Variables(1).ValuesAsNumpy().tolist()
#         hourly_json_data['hourly_apparent_temperature'] = hourly.Variables(2).ValuesAsNumpy().tolist()
#         hourly_json_data['hourly_rain'] = hourly.Variables(3).ValuesAsNumpy().tolist()
#         hourly_json_data['hourly_surface_pressure'] = hourly.Variables(4).ValuesAsNumpy().tolist()
#         hourly_json_data['hourly_wind_speed_10m'] = hourly.Variables(5).ValuesAsNumpy().tolist()
#         hourly_json_data['hourly_wind_direction_10m'] = hourly.Variables(6).ValuesAsNumpy().tolist()
#         return hourly_json_data   
#     def _json_daily(self):
#         daily_json_data = {}
#         daily = self._class.Daily()
#         daily_json_data["date"] = pd.date_range(
#         start=pd.to_datetime(daily.Time(), unit="s"),
#         end=pd.to_datetime(daily.TimeEnd(), unit="s"),
#         freq=pd.Timedelta(seconds=daily.Interval())
#     ).to_pydatetime().tolist()
#         daily_json_data["temperature_2m_max"] = daily.Variables(0).ValuesAsNumpy().tolist()
#         daily_json_data["temperature_2m_min"] = daily.Variables(1).ValuesAsNumpy().tolist()
#         return daily_json_data
#     def get_temperature_hourly(self):
#         temperature = self._hourly_return["hourly_temperature_2m"]
#         date = self._hourly_return["date"]
#         temp_values = []
#         date_values = []
#         format = '%Y-%m-%d %H:%M:%S'
#         current_time = datetime.now()
#         end_time = current_time + timedelta(hours=24)
#         for index, value in enumerate(date):
#             if current_time < value <=end_time:
#                 temp_values.append(temperature[index])
#                 date_values.append(value.strftime(format))
#         return {'temperature':temp_values, 'labels':date_values}
#     def get_temperature_hourly_modal(self):
#         temperature = self._hourly_return["hourly_temperature_2m"]
#         divided_temperature_list = [temperature[i:i+24] for i in range(0, len(temperature), 24)]
#         print(divided_temperature_list)
#     def get_humidity_hourly(self):
#         pass

