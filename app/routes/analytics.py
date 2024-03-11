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

@analytics_bp.route('/<id>/<device>/hourly')
@login_required
def analytics_hourly(id, device):
    id = int(id)
    if current_user.id == id:
        darla = Darla.query.filter_by(device_id = device).first()
        now = datetime.now()
        day_start = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
        local_list = []
        forecast_list = []
        data = {}
        if darla:
            all_local = Data.query.filter_by(darla_id = darla.id).filter(and_(Data.date_added> day_start, Data.date_added<= day_start+ timedelta(hours=24))).all()
            all_forecast = Hourly.query.filter_by(darla_id = darla.id).filter(and_(Hourly.date_forecast > now, Hourly.date_forecast <= day_start+timedelta(hours=24))).all()
            for fore, loc in zip_longest(all_forecast, all_local):
                if loc:
                    local_list.append(loc.date_added)
                if fore:
                    forecast_list.append(fore.date_forecast)
                    # A return statement to be added
            return data
        else:
            abort(404)
    else:
        abort(401)
