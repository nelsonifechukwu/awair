from flask import Blueprint,render_template, redirect, request, session,flash
from ..extensions import *
from ..models.user import *
from ..models.device import *
from config import Config
from ..passwords import Password
from ..resource import *
from oauthlib import oauth2
import requests
import json





# Implement LOGGING

# add timing to sessions must be done and session id !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) 



client = oauth2.WebApplicationClient(Config.CLIENT_ID)
# would add error handling and logging to this function!!!!

def get_google_provider_cfg():
    return requests.get(Config.GOOGLE_DISCOVERY_URL).json()

auth = Blueprint('auth', __name__)
@auth.route("/")
@auth.route("/signup", methods=['GET', 'POST'])
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
@auth.route("/login", methods= ['POST'])
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
            # session.permanent = True
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
    


@auth.route("/googlelogin")
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
    
@auth.route("/googlelogin/callback")
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
        # session.permanent = True
        return redirect(f"/dashboard/{user.id}")
    else:
        return "User email not available or not verified by Google.", 400

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/signup"), 302