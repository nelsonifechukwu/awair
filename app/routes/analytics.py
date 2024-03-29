from flask import Blueprint,render_template, redirect, request, session,flash, abort
from ..extensions import *
from ..models.user import *
from ..models.data import *
from ..models.device import *
from ..models.forecast import *
from config import Config
from ..passwords import Password
from ..resource import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
from sqlalchemy import desc, and_, or_
from ..functions import Funcs
from itertools import zip_longest
import random

analytics_bp = Blueprint('analytics_bp', __name__, url_prefix='/analytics')

# Apply caching on this route !!!!!!!!!!!
def make_cache_key(*args, **kwargs):
    cache_key = request.full_path
    return cache_key

@analytics_bp.route('/<id>/<device>/hourly')
@login_required
@cache.memoize(timeout=300, make_name=make_cache_key)
def analytics_hourly(id, device):
    data = request.query_string.decode()
    data = data.split(',')
    para = data[0]
    id = int(id)
    if current_user.id == id:
        darla = Darla.query.filter_by(device_id = device).first()
        now = datetime.now()
        day_start = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
        forecast_list = []
        forecast_date = []
        forecast = {}
        if darla:
            if data:
                # Add error checking here
                data = int(data[1])
                all_forecast = Hourly.query.filter_by(darla_id = darla.id).filter(and_(Hourly.date_forecast > day_start+timedelta(hours =24*(data-1) ), Hourly.date_forecast <= day_start+timedelta(hours=24*data))).all()
            for fore in all_forecast:
                if fore:
                    if para == 'temp':
                        forecast_list.append(fore.temperature_2m)
                    elif para == 'hum':
                        forecast_list.append(fore.relative_humidity_2m)
                    elif para == 'pressure':
                        forecast_list.append(fore.surface_pressure)
                    elif para == 'feel':
                        forecast_list.append(fore.apparent_temperature)
                    elif para == 'rain':
                        forecast_list.append(fore.rain)
                    elif para == 'wind':
                        wind_data = {'speed':fore.wind_speed_10m, 'direction': (fore.wind_direction_10m)}
                        forecast_list.append(wind_data)
                    forecast_date.append(fore.date_forecast)
            forecast['data'] = forecast_list
            forecast['date'] = forecast_date
            forecast['now'] = datetime.now().strftime("%Y-%m-%d %H:%M%:%S")
            forecast["strdate"] = forecast_date[2].strftime('%A, %d %b %Y')
            # print(num)
            
            return forecast
        else:
            abort(404)
    else:
        abort(401)

@analytics_bp.route('/<id>/<device>/check')
@login_required
def check_time(id, device):
    data = request.query_string.decode()
    id = int(id)
    datas = {}
    if current_user.id == id:
        darla = Darla.query.filter_by(device_id= device).first()
        now = datetime.now()
        day_start = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
        if data:
            data = int(data)
            strftime = Hourly.query.filter_by(darla_id = darla.id).filter(and_(Hourly.date_forecast > day_start+timedelta(hours =24*(data-1) ), Hourly.date_forecast <= day_start+timedelta(hours=24*data))).first()
            datas['date'] = strftime.date_forecast.strftime('%A, %d %b %Y')
        return datas
    else:
        abort(401)