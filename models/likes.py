from datetime import datetime
from db import db

class LikeModel(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key = True) 
    user = db.Column(db.String(80))
    flag = db.Column(db.Integer())
    date = db.Column(db.Date(), default = datetime.now().date())

    post_id = db.Column(db.Integer, db.ForeignKey ('posts.id'))
    posts = db.relationship('PostModel')


    def __init__(self, post_id, user, flag):
        self.post_id = post_id
        self.user = user
        self.flag = flag

    @classmethod
    def find_by_post_id(cls, post_id):  # finding post by ID, if it exist
        return cls.query.filter_by(post_id = post_id).all()

    @classmethod
    def find_by_name(cls, user):    # finding user like by username, if it exist
        return cls.query.filter_by(user = user).first()

    @classmethod
    def find_by_date(cls, date):
       return cls.query.filter_by(date = date).all()

    def save_like(self):   # inserting and updating data to database
        db.session.add(self)
        db.session.commit()

    def delete_like(self):   # removing like from post
        db.session.delete(self)
        db.session.commit()