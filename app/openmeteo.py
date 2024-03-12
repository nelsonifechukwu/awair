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
    def __init__(self,lat,lon, device_id, url = "https://api.open-meteo.com/v1/forecast", client = pymongo.MongoClient(Config.MONGO_DATABASE_URL)[Config.MONGO_DB][Config.MONGO_COL]):
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
    # Mongo's idea is proving difficult to use So might use relational db for now to accomplish my goal (I could opt for a better architecture which is what I'll most likely do as well)
    def store_data(self):
        response = self._api_req()
        response_dump = pickle.dumps(response)
        response_dict = self.convert_to_dict(response_dump)
        self._client.update_one({'_id':self._device},{'$set':response_dict},upsert=True)
        return "Updated"
    
   
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
    
    