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

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in_y = db.Column(db.Integer)
    check_in_m = db.Column(db.Integer)
    check_in_d = db.Column(db.Integer)
    check_out_y = db.Column(db.Integer)
    check_out_m = db.Column(db.Integer)
    check_out_d = db.Column(db.Integer)
    chk_in_full = db.Column(db.String(125))
    chk_out_full = db.Column(db.String(125))
    total_days = db.Column(db.Integer)
    reserved_by = db.Column(db.Integer)
    reserved_by_user = db.Column(db.String(125))
    reserved_room = db.Column(db.Integer)
    reserved_room_title = db.Column(db.String(125))
    reserved_room_thumb = db.Column(db.String(125))
    reserved_room_price = db.Column(db.String(125))
    expire_date = db.Column(db.String(125))