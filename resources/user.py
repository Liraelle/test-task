from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', 
                    type = str, 
                    required = True, 
                    help = "This area cannot be left blank!")
_user_parser.add_argument('password', 
                    type = str, 
                    required = True, 
                    help = "This area cannot be left blank!")

class UserRegister(Resource):   # singing up 
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with this username already exist.'}, 400


        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class UserLogin(Resource):  # loging in 
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and user.password == data['password']:  # this is authenticate
            access_token = create_access_token(identity = user.id, fresh = True)    # this is identity
            user.logtime = datetime.now()   # when user was login last time
            user.save_to_db()
            
            return{
                'access_token': access_token
                }, 200
        return {'message': 'Invalid credenrials'}, 401
