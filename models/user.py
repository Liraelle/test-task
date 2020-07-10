import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users' # creating table in database
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    logtime = db.Column(db.DateTime(timezone=True)) # date, when user login last time
    reqtime = db.Column(db.DateTime(timezone=True)) # date, when user made a last request to service

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def save_to_db(self):   # saving user credentials in database
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):    # finding user by username
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls, _id):   # finding user by id
        return cls.query.filter_by(id = _id).first()
