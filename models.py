from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from exts import db


# 模型映射
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    is_admin = db.Column(db.Integer, nullable=False)



class Area(db.Model):
    __tablename__ = "area"
    area_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area_name = db.Column(db.String(20), nullable=False)
    area_range = db.Column(db.Float, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Float, nullable=False)


class Fellow(db.Model):
    __tablename__ = "fellow"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fellow_name = db.Column(db.String(20), nullable=False)
    fellow_phone = db.Column(db.String(20), nullable=False)
    fellow_sex = db.Column(db.String(30), nullable=False)
    fellow_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    fellow = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Float, nullable=False)
    time = db.Column(db.String(20), nullable=False)
    data_area = db.Column(db.String(20), nullable=False)
