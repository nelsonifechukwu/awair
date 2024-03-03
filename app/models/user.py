from ..extensions import db, UserMixin
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key = True)
    username = db.Column(db.String(30), nullable=False, unique = True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    key = db.Column(db.String(120), nullable=False)
    # add profile picture (Optional) more than 20 for google sign in !!!!!!!!!!!!!!!!!!!!!!
    profile_picture = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.now)
    uuid = db.relationship('Uuid', backref=db.backref('Uuid'))


class Uuid(db.Model):
    uuid_id = db.Column(db.Integer, nullable=False, primary_key=True)
    uuid = db.Column(UUID(as_uuid = True), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.now)