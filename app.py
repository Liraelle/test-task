from flask import Flask
from flask_restful import  Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserLogin
from resources.posts import Post, PostCheck, PostList
from resources.likes import Likes
from resources.analytics import Analytics
from db import db
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Nata'
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

jwt = JWTManager(app)

api.add_resource(Post, '/posts/<string:name>')
api.add_resource(PostCheck, '/posts/<string:_id>')
api.add_resource(PostList, '/posts')
api.add_resource(UserRegister, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(Likes, '/posts/<string:name>/likes')
api.add_resource(Analytics, '/api/analitics/')

if __name__ == '__main__':
    db.init_app(app)
    app.run()