from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.Text)
    avatar = db.Column(db.String(225), default="default_user_img.png")
    role = db.Column(db.Boolean(), default=False)
    registered_on = db.Column(db.DateTime, default=datetime.now())


