from flask import Blueprint,render_template, redirect, request, session,flash
from .extensions import *
from .models import *
from config import Config
from .passwords import Password
from .resource import *
from oauthlib import oauth2
from werkzeug.utils import secure_filename
import requests
import json
import os
from datetime import datetime, timedelta
from sqlalchemy import desc
#Look for something else other than geopy !!!!!!!!!!!!!!!!!!!!!!!!! 

# Implement LOGGING

# add timing to sessions must be done and session id !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) 

api.add_resource(TempData,"/temp")
api.add_resource(WindData,"/wind")
api.add_resource(RainData,"/rain")
api.add_resource(LocationData,"/location")
api.add_resource(AirQualityData, "/airqo")

client = oauth2.WebApplicationClient(Config.CLIENT_ID)
# would add error handling to this function!!!!

def get_google_provider_cfg():
    return requests.get(Config.GOOGLE_DISCOVERY_URL).json()

# USE CLASSES FOR TYPE CHECKING INSTEAD OF JUST PURE EXCEPTIONS.

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

def convert_int(string):
    return int(string)

def files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.EXTS

main = Blueprint('main', __name__)
@main.route("/")
@main.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).all()
        user_email = User.query.filter_by(email=email).all()
        if not user and not user_email:
            # Verification with Email to be done !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            key, password = Password().encrypt_password(password)
            new = User(username= username, name=name, email=email, password= password, key=key)
            db.session.add(new)
            db.session.commit()
            return redirect("/signup"), 301
        else:
            flash("Username/ Email already exists. Please Login", "danger")
            return redirect('/signup')
    if current_user.is_authenticated:
        return redirect(f"/dashboard/{current_user.id}")
    return render_template("signup.html"), 200
@main.route("/login", methods= ['POST'])
def login():
    # get form data
    username = request.form['username']
    password = request.form['password']
    if "@" in list(username):
        user = User.query.filter_by(email = username).first()
    else:
        user = User.query.filter_by(username=username).first()
    
    if user is None:
        flash("No such username or email. Register", "danger")
        return redirect('/signup'), 301
    else:
        decrypted_pass = Password(user.key).decrypt_password(user.password)
        # print(decrypted_pass)
        if password == decrypted_pass:
            # session["loggedin"] = True
            login_user(user)
            id = Uuid.query.filter_by(user_id = user.id).first()
            # print(id)
            if id is None:
                return redirect(f'/dashboard/{user.id}'), 302
            else:
                device = Darla.query.filter_by(id = id.uuid).first()
                return redirect(f'/dashboard/{user.id}/{device.device_id}'),302
        else:
            flash("Incorrect Password", "danger")
            return redirect("/signup"), 301
    


@main.route("/googlelogin")
def googlelogin():
    try:
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
        )
        return redirect(request_uri), 302
    except:
        flash("HTTPs connection error: please check your network", "danger")
        return redirect("/login")
    
@main.route("/googlelogin/callback")
def googlelogincallback():
    
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )
    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(Config.CLIENT_ID, Config.CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        picture = userinfo_response.json()["picture"]
        user = User.query.filter_by(username=unique_id).first()
        # print(user)
        if user is None:
            new = User(username=unique_id, email=users_email, name=users_name, password="none", key="none", profile_picture=picture)
            db.session.add(new)
            db.session.commit()
        login_user(user)
        return redirect(f"/dashboard/{user.id}")
    else:
        return "User email not available or not verified by Google.", 400

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/signup"), 302

    
#ERROR HANDLING FOR POST ROUTES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
# Session API needs to be checked out "https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get" because Query.get() not in sqlalchemy 2.x
@main.route('/dashboard/<id>', methods=["GET","POST"])
@login_required
def dashboard(id):
    try:
        id = int(id)
        if current_user.id == id:
            user = db.session.get(User, id)
            uuid_ex = Uuid.query.filter_by(user_id = id).join(Darla, Darla.id == Uuid.uuid).add_columns(Darla.device_id).first()
            # uuid_ex = db.session.query(Uuid, Darla.device_id).filter(Uuid.user_id == id).join(Darla, Darla.id == Uuid.uuid).first()
            if request.method == 'POST':
                uuid_val = request.form["uuid"]
                darla = Darla.query.filter_by(device_id = uuid_val).first() 
                if darla:
                    is_uuid = Uuid.query.filter_by(uuid=darla.id).first()
                    if not is_uuid:
                        new = Uuid(uuid = darla.id, user_id=id)
                        db.session.add(new)
                        db.session.commit()
                        return redirect(f"/dashboard/{id}/{darla.device_id}#data"),302
                    else:
                        flash("Device already registered", "danger")
                        return redirect(f"{request.url}"),302
                else:
                    flash("Error Adding Device", "danger")
                    return redirect(f"{request.url}"),302
            if uuid_ex:
                return redirect(f"/dashboard/{id}/{uuid_ex.device_id}#data"), 302
            else:
                return render_template("dashboard.html", user=user, no_of_device = 0)  
        else:
            # abort(404)
            return redirect(f"/dashboard/{current_user.id}#data")
    except ValueError:
        abort(400) 


@main.route("/dashboard/<id>/profile/upload", methods=["POST"])
@login_required
def upload_picture(id):
    id = int(id)
    if current_user.id == id:
        user = db.session.get(User, id)
        try:
            profile = request.files["profile"]
            if profile.filename == '':
                flash("Please put a valid file", "danger")
                return "Invalid", 403
            else:
                if profile.filename and files(profile.filename):
                    if user.profile_picture:
                        if os.path.exists(Config.UPLOADS + user.profile_picture):
                            os.remove(os.path.join(
                            Config.UPLOADS, user.profile_picture))
                    filename = secure_filename(profile.filename)
                    filename = f"{id}__{filename}"
                    # print(os.path.join(Config.UPLOADS, filename))
                    profile.save(os.path.join(Config.UPLOADS, filename))
                    user.profile_picture = filename
                    db.session.commit()
                    flash("Photo added successfully","success")
                    return "created", 201
                else:
                    flash("Invalid file type", "danger")
                    return "Invalid", 403
        except Exception as e:
            print(e)
            abort(400), "Please enter a file"
    else:
        abort(401)

# Use Exceptionnssssssss!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@main.route("/dashboard/<id>/profile/remove")
@login_required
def remove_picture(id):
    id = int(id)
    if current_user.id == id:
        user = db.session.get(User, id)
        if os.path.exists(Config.UPLOADS + user.profile_picture):
            os.remove(os.path.join(
                    Config.UPLOADS, user.profile_picture))
            user.profile_picture = None
            db.session.commit()
            return redirect(f"/dashboard/{user.id}#account"),302 
    else:
        abort(401)
        
@main.route("/dashboard/<id>/profile/edit", methods = ["POST"])
@login_required
def edit_profile(id):
    id = int(id)
    if current_user.id == id:
        user = db.session.get(User, id)
        name = request.form["name"]
        username = request.form["username"]
        is_username = User.query.filter_by(username=username).first()
        user.name = name
        if is_username and (username != user.username):
            flash("Username already taken", "danger")     
        else:
            user.username = username
            flash("Username already changed", "success")
        db.session.commit()
        return redirect(f"/dashboard/{user.id}#account")
    else:
        abort(401)
@main.route("/dashboard/<id>/profile/password/change", methods = ["POST"])
@login_required
def change_password(id):
    id = int(id)
    if current_user.id == id:
        user = db.session.get(User, id)
        current = request.form["current"]
        new = request.form["new"]
        retype = request.form["retype"]
        current_password = Password(user.key).decrypt_password(user.password)
        # print(current_password)
        if current == current_password:
            if new == retype:
                if new != current_password:
                    new_key,new_password  = Password().encrypt_password(new)
                    user.key = new_key
                    user.password = new_password
                    db.session.commit()
                    flash("Password changed successfully","success")
                else:
                    flash("New password cannot be the same as old ", "info")
            else:
                flash("Password typed mismatch", "danger")
        else:
            flash("Invalid current password. Please do account recovery in the occasion you don't remember your password.", "danger")
        return redirect(f"/dashboard/{user.id}")
    else:
        abort(401)
        





# Responsiveness is S*** !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Total number of device to be added to the user table (To avoid the justin beiber problem)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Devices
@main.route("/dashboard/<id>/<device>", methods=["GET","POST"])
@login_required
def dashboard_user(id, device):
    try:
        id = int(id)
        if current_user.id == id:
            user = db.session.get(User, id)
            darla = Darla.query.filter_by(device_id = device).first()
            location = None
            if request.method == "POST":
                device_val = request.form["device_id"]
                darla = Darla.query.filter_by(device_id = device_val).first() 
                if darla:
                    is_uuid = Uuid.query.filter_by(uuid=darla.id).first()
                    if not is_uuid:
                        new = Uuid(uuid=darla.id, user_id = id)
                        db.session.add(new)
                        db.session.commit()
                        return redirect(f"/dashboard/{id}/{darla.device_id}#devices"), 302
                    else:
                        flash("Device already registered", "danger")
                        return redirect(f"{request.url}#devices"),302
                else:
                    flash("Error Adding Device", "danger")
                    return redirect(f"{request.url}#devices"),302 
            
            if darla:
                device_all = Uuid.query.filter_by(user_id =id).join(Darla, Uuid.uuid == Darla.id).add_columns(Darla.device_id, Uuid.date_added, Darla.active, Darla.last_updated, Darla.place, Darla.battery, Darla.signal).all()
                no_of_device =len(device_all)
                location = darla.location
                lat = 0
                long =0
                if location:
                    loc = location.split(",")
                    lat = loc[0]
                    long = loc[1]
                is_device = Uuid.query.filter_by(user_id =id).first()
                if is_device:
                    # print(darla.active)
                    return render_template("dashboard_user.html", user=user, device = device_all, darla=darla, location=location, lat = lat, long=long, dev=device,airq=0, tph_data=0, wind=0, precipitation=0, no_of_device = no_of_device)
                else:
                    return redirect(f"/dashboard/{user.id}")
            else:
                abort(404)
        else:
            return redirect("/signup")
    except ValueError:
        abort(400)

@main.route("/dashboard/<id>/<device>/status")
@login_required
def change_status(id, device):
    index = request.query_string.decode()
    id = int(id)
    if current_user.id == id:
        darla = Darla.query.filter_by(device_id = device).first()
        try:
            now = datetime.now()
            time_diff = darla.last_updated + timedelta(hours=1)
            if now > time_diff:
                darla.active = 0
            else:
                darla.active = 1
            db.session.commit()
        except Exception as e:
            print(e)
        if 'hx_request' in request.headers: 
            return render_template('status.html', id = darla, index=index)
        else:
            abort(404)
    else:
        abort(404)
        
@main.route("/dashboard/<id>/<device>/listdata")
@login_required
def change_battery(id, device):
    index = request.query_string.decode()
    id = int(id)
    if current_user.id == id:
        darla = Darla.query.filter_by(device_id = device).first()
        try:
            now = datetime.now()
            time_diff = darla.last_updated + timedelta(hours=1)
            if now > time_diff:
                darla.active = 0
            else:
                darla.active = 1
            db.session.commit()
        except Exception as e:
            print(e)
        if 'hx_request' in request.headers: 
            return render_template('listbattery.html', darla = darla, index=index)
        else:
            abort(404)
    else:
        abort(404)

@main.route("/dashboard/<id>/<device>/remove")
@login_required
def remove_device(id, device):
    id = int(id)
    if current_user.id == id:
        darla = Darla.query.filter_by(device_id = device).first()
        if darla:
            device_uuid = Uuid.query.filter_by(uuid=darla.id).first()
            if device_uuid:
                device_uuid.user_id = None
                db.session.delete(device_uuid)
                db.session.commit()
                flash("Device successfully removed","success")
        return redirect(f"/dashboard/{id}/{darla.device_id}#devices")
    else:
        abort(403)
# Maps
@main.route("/dashboard/<id>/map/all")
def all_parameters(id):
    id = int(id)
    if current_user.id == id:
        all_data = {}
        all_uuid = Uuid.query.filter_by(user_id = id).all()
        if all_uuid:
            for a_uuid in all_uuid:
                darla = Darla.query.filter_by(id = a_uuid.uuid).first()
                tph = Data.query.order_by(desc(Data.date_added)).filter_by(darla_id = a_uuid.uuid).first()
                wind = Wind.query.order_by(desc(Wind.date_added)).filter_by(darla_id = a_uuid.uuid).first()
                air = AirQuality.query.order_by(desc(AirQuality.date_added)).filter_by(darla_id = a_uuid.uuid).first()
                if (darla and wind) and (air and tph):
                    all_data[f"{darla.device_id}"] = {'temperature':tph.temperature, 'humidity': tph.humidity, 'pressure':tph.pressure, 'wind_speed': wind.wind_speed, 'wind_direction': wind.wind_direction, 'pmtwo':air.pmtwo, 'pmten': air.pmten, 'co':air.co_index, 'place':darla.place}
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return all_data
    else:
        abort(401)

# Map devices
@main.route("/dashboard/<id>/locations")
@login_required
def get_location(id):
    id = int(id)
    if current_user.id == id:
        latlongs = {}
        all_uuid = Uuid.query.filter_by(user_id = id).all()
        if all_uuid:
            for a_uuid in all_uuid:
                
                darla = Darla.query.filter_by(id = a_uuid.uuid).first()
                device_location = darla.location
                if device_location:
                    lat = device_location.split(",")[0]
                    long = device_location.split(",")[1]
                    latlongs[f"{darla.device_id}"] = {"lat":lat, "long":long}

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return latlongs 
        else:
            abort(404)

    else:
        abort(401)

# LISTS
        # make lists all 1 hx-request !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@main.route("/dashboard/<id>/<device>/airquality")
@login_required
def get_airquality(id, device):
    id = int(id)
    if current_user.id == id:
        diff = 0
        user = db.session.get(User, id)
        device = Darla.query.filter_by(device_id = device).first()
        if device:
            airquality_data = AirQuality.query.order_by(desc(AirQuality.date_added)).filter_by(darla_id = device.id).first()
            if airquality_data:
                diff = convert_timedelta(airquality_data.date_added)
            if 'hx_request' in request.headers:
                return render_template("airquality.html", airq = airquality_data, device=device, user=user, diff=diff)
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(403)



@main.route("/dashboard/<id>/<device>/tph")
@login_required
def get_tph(id, device):
    id = int(id)
    if current_user.id == id:
        user = db.session.get(User, id)
        device = Darla.query.filter_by(device_id = device).first()
        diff = 0
        if device:
            tph_data = Data.query.order_by(desc(Data.date_added)).filter_by(darla_id = device.id).first()
            if tph_data:
                diff = convert_timedelta(tph_data.date_added)
            
            if 'hx_request' in request.headers:
                return render_template("tph.html", tph_data = tph_data, device=device, user=user, diff = diff)
            elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if tph_data:
                    return {'temperature':tph_data.temperature, 'humidity':tph_data.humidity, 'pressure':tph_data.pressure}
                else:
                    return {'temperature':0, 'humidity':0, 'pressure':0}
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(403)

@main.route("/dashboard/<id>/<device>/precipitation")
@login_required
def get_precipitation(id, device):
    id = int(id)
    if current_user.id == id:
        diff = 0
        user = db.session.get(User, id)
        device = Darla.query.filter_by(device_id = device).first()
        if device:
            precipitation = Rain.query.order_by(desc(Rain.date_added)).filter_by(darla_id = device.id).first()
            if precipitation:
                diff = convert_timedelta(precipitation.date_added)
            if 'hx_request' in request.headers:
                return render_template("precipitation.html", precipitation = precipitation, device=device, user=user, diff=diff)
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(403)

@main.route("/dashboard/<id>/<device>/wind")
@login_required
def get_wind(id, device):
    id = int(id)
    if current_user.id == id:
        diff = 0
        user = db.session.get(User, id)
        device = Darla.query.filter_by(device_id = device).first()
        if device:
            wind = Wind.query.order_by(desc(Wind.date_added)).filter_by(darla_id = device.id).first()
            if wind:
                diff = convert_timedelta(wind.date_added)
            if 'hx_request' in request.headers:
                return render_template("wind.html", wind = wind, device=device, user=user, diff=diff)
            elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if wind:
                    return {'speed':wind.speed, 'direction':wind.direction, 'cloud_cover':wind.cloud_cover}
                else:
                    return {'speed':0, 'direction':0, 'cloud_cover':0}
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(403)

# Link to session timing: https://flask.palletsprojects.com/en/3.0.x/config/#PERMANENT_SESSION_LIFETIME
        
# CHARTS
# For TPH
# Use Query strings instead of routes for weeks !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@main.route("/dashboard/<id>/<device>/charts/<week>/tph")
@login_required
def graph_tph(id, device, week):
    id = int(id)
    week =int(week)
    if current_user.id == id:
        labels = []
        temp_list = []
        hum_list = []
        press_list = []
        all_data = {}
        format = '%Y-%m-%d %H:%M:%S'
        current_time = datetime.now()
        if week ==1 or week == 7:
            time_diff = current_time-timedelta(days=week)
        else:
            time_diff = current_time - timedelta(weeks=week)
        this_device = Darla.query.filter_by(device_id = device).first()
        if this_device:
            tph_data = Data.query.filter_by(darla_id = this_device.id).filter(Data.date_added>time_diff).all()
            
            for t in tph_data:
                temp = float(t.temperature)
                temp_list.append(temp)
                hum = float(t.humidity)
                hum_list.append(hum)
                press = float(t.pressure)
                press_list.append(press)
                date_string = t.date_added.strftime(format)
                labels.append(date_string)
            all_data['temperature_data'] = temp_list
            all_data['humidity_data'] = hum_list
            all_data['pressure_data'] = press_list
            all_data['labels'] = labels
        
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return all_data
        
        else:
            abort(404)
    else:
        abort(401)
@main.route("/dashboard/<id>/<device>/charts/tph/latest")
@login_required
def latest_tph(id, device):
    id = int(id)
    if current_user.id == id:
        date_data = {}
        format = '%Y-%m-%d %H:%M:%S'
        this_device = Darla.query.filter_by(device_id = device).first()
        if this_device:
            date_added = Data.query.order_by(desc(Data.date_added)).filter_by(darla_id = this_device.id).first()
            if date_added:
                temperature = float(date_added.temperature)
                date_data['temperature'] = temperature
                humidity = float(date_added.humidity)
                date_data['humidity'] = humidity
                pressure = float(date_added.pressure)
                date_data['pressure'] = pressure
                date_data['date_added'] = date_added.date_added.strftime(format)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return date_data
        else:
            abort(404)
    else:
        abort(401)

# For Wind
@main.route("/dashboard/<id>/<device>/charts/<week>/wind")
@login_required
def graph_wind(id,device,week):
    id =int(id)
    week = int(week)
    if current_user.id == id:
        format = '%Y-%m-%d %H:%M:%S'
        wind_data = []
        current_time = datetime.now()
        if week ==1 or week == 7:
            time_diff = current_time-timedelta(days=week)
        else:
            time_diff = current_time - timedelta(weeks=week)
        this_device = Darla.query.filter_by(device_id = device).first()
        if this_device:
            wind_instances = Wind.query.filter_by(darla_id = this_device.id).filter(Wind.date_added>time_diff).all()
            for wind in wind_instances:
                data = {'date':wind.date_added.strftime(format),'speed':int(wind.wind_speed), 'direction': int(wind.wind_direction)}
                wind_data.append(data)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
           return wind_data
        else:
           abort(404)
    else:
       abort(401)

@main.route("/dashboard/<id>/<device>/charts/wind/latest")
@login_required
def latest_wind(id, device):
    id = int(id)
    if current_user.id == id:
        data = {}
        format = '%Y-%m-%d %H:%M:%S'
        this_device = Darla.query.filter_by(device_id = device).first()
        data = ""
        if this_device:
            wind = Wind.query.order_by(desc(Wind.date_added)).filter_by(darla_id = this_device.id).first()
            if wind:
               data = {'date':wind.date_added.strftime(format),'speed':int(wind.wind_speed), 'direction': int(wind.wind_direction)}
            else:
                data = {'date':0,'speed':0, 'direction': 0}
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return data
        else:
            abort(404)
    else:
        abort(401)

# For Air Quality

@main.route("/dashboard/<id>/<device>/charts/<week>/air")
@login_required
def graph_air(id, device, week):
    id = int(id)
    week =int(week)
    if current_user.id == id:
        labels = []
        pmtwo_list = []
        pmten_list = []
        co_list = []
        all_data = {}
        format = '%Y-%m-%d %H:%M:%S'
        current_time = datetime.now()
        if week ==1 or week == 7:
            time_diff = current_time-timedelta(days=week)
        else:
            time_diff = current_time - timedelta(weeks=week)
        this_device = Darla.query.filter_by(device_id = device).first()
        if this_device:
            tph_data = AirQuality.query.filter_by(darla_id = this_device.id).filter(AirQuality.date_added>time_diff).all()
            
            for t in tph_data:
                pmtwo = float(t.pmtwo)
                pmtwo_list.append(pmtwo)
                pmten = float(t.pmten)
                pmten_list.append(pmten)
                co_index = float(t.co_index)
                co_list.append(co_index)
                date_string = t.date_added.strftime(format)
                labels.append(date_string)
            all_data['pmtwo_data'] = pmtwo_list
            all_data['pmten_data'] = pmten_list
            all_data['co_data'] = co_list
            all_data['labels'] = labels
        
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return all_data
        
        else:
            abort(404)
    else:
        abort(401)
@main.route("/dashboard/<id>/<device>/charts/air/latest")
@login_required
def latest_air(id, device):
    id = int(id)
    if current_user.id == id:
        date_data = {}
        format = '%Y-%m-%d %H:%M:%S'
        this_device = Darla.query.filter_by(device_id = device).first()
        if this_device:
            date_added = AirQuality.query.order_by(desc(AirQuality.date_added)).filter_by(darla_id = this_device.id).first()
            if date_added:
                pmtwo = float(date_added.pmtwo)
                date_data['pmtwo'] = pmtwo
                pmten = float(date_added.pmten)
                date_data['pmten'] = pmten
                co = float(date_added.co_index)
                date_data['co'] = co
                date_data['date_added'] = date_added.date_added.strftime(format)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return date_data
        else:
            abort(404)
    else:
        abort(401)

# For analytics
# Averages
# Wind rose charts to show wind speed and direction
# Comparison
# Plot graphs against each other. The user decides (Playground)
        
# Testing
# Number of devices on Map
# Styling of sidebar
# Design of device details on map
