from db import db

class PostModel(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(80))
    post = db.Column(db.String(500))

    likes = db.relationship('LikeModel')

    def __init__(self, name, post):
        self.name = name
        self.post = post

    def json(self):
        return {'post_id': self.id, 'name': self.name, 'post': self.post}

    @classmethod    # finding post by name
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    @classmethod    # finding post by id
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    def save_post_to_db(self):   # inserting and updating data to database
        db.session.add(self)
        db.session.commit()

    def delete_like(self):   # removing like from post
        db.session.delete(self)
        db.session.commit()