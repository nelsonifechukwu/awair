import requests
from config import Config
from datetime import datetime, timedelta
class Funcs:
    @staticmethod
    def convert_timedelta(date):
        if date:
            date = datetime.now() - date
            day = date.days
            hours = date.seconds//3600
            minutes = (date.seconds//60)%60
            seconds = date.seconds
            if date <timedelta(minutes=1):
                diff = f"{seconds} seconds ago"
            elif date < timedelta(hours=1):
                diff = f"{minutes} minutes ago"
            elif date < timedelta(days=1):
                diff = f"{hours} hours ago" 
            else:
                diff = f"{day} days ago"
            return diff
        else:
            return "None"
    @staticmethod
    def convert_float(string):
        return float(string)
    @staticmethod
    def convert_int(val):
        return int(val)
    @staticmethod
    def files(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.EXTS
