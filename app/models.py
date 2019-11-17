from app import db

class User(db.Model):
    """
    登陆
    """
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(100))
    password = db.Column(db.String(100))