from flask import Blueprint,render_template, redirect, request, session,flash, abort
from ..extensions import *
from ..models.user import *
from ..models.data import *
from ..models.device import *
from config import Config
from ..passwords import Password
from ..resource import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
from sqlalchemy import desc
from ..functions import Funcs

analytics_bp = Blueprint('analytics_bp', __name__, url_prefix='/analytics')

