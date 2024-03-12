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

analytics_bp = Blueprint('analytics_bp', __name__, url_prefix='/analytics')

# Apply caching on this route !!!!!!!!!!!
@analytics_bp.route('/<id>/<device>/hourly')
@login_required
def analytics_hourly(id, device):
    data = request.query_string.decode()
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
                data = int(data)
                all_forecast = Hourly.query.filter_by(darla_id = darla.id).filter(and_(Hourly.date_forecast > day_start+timedelta(hours =24*(data-1) ), Hourly.date_forecast <= day_start+timedelta(hours=24*data))).all()
            for fore in all_forecast:
                if fore:
                    forecast_list.append(fore.temperature_2m)
                    forecast_date.append(fore.date_forecast)
            forecast['data'] = forecast_list
            forecast['date'] = forecast_date
            forecast['now'] = datetime.now().strftime("%Y-%m-%d %H:%M%:%S")
            return forecast
        else:
            abort(404)
    else:
        abort(401)

