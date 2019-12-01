from app import db
import datetime


class User(db.Model):
    """登陆"""
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Traffic(db.Model):
    """用户访问量"""
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    city = db.Column(db.String(100))
    pv = db.Column(db.Integer,default=0)
    uv = db.Column(db.Integer,default=0)
    date = db.Column(db.Date,default=datetime.datetime.now)


class SensitiveWord(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    word = db.Column(db.Text)


class Image(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(200))

