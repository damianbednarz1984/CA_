from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(100), default="")
    gender = db.Column(db.String(100), default="")
    country = db.Column(db.String(100), default="")
    city = db.Column(db.String(100), default="")
    zip_code = db.Column(db.String(100), default="")
    address = db.Column(db.Text, default="")
    date_of_birth = db.Column(db.String(100), default="")
    password = db.Column(db.Text)
    avatar = db.Column(db.String(225), default="default_user_img.png")
    role = db.Column(db.Boolean(), default=False)
    registered_on = db.Column(db.DateTime, default=datetime.now())


class Rooms(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	description = db.Column(db.Text)
	thumb = db.Column(db.String(225))
	price = db.Column(db.Integer)
	bed = db.Column(db.Integer)
	lunch = db.Column(db.Boolean(), default=False)
	wifi = db.Column(db.Boolean(), default=False)