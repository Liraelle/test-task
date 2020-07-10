from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, jwt_optional, get_jwt_identity)
from models.posts import PostModel
from models.user import UserModel
from datetime import datetime

def user_activity():    # when user made a last request to service
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if user:
            user.reqtime = datetime.now()
            user.save_to_db()

class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('post',
                        type = str, 
                        required = True, 
                        help = "This area cannot be left blank!")

    @jwt_required   # JWT authentication
    def get (self, name):   # checking if post exist
        user_activity()

        item = PostModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': 'Post not found'}, 404 

    @jwt_required
    def post(self, name):   # post creation
        user_activity()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'messsage': 'Unregistered user. Access denied.'}

        if PostModel.find_by_name(name):  # checking if post exist
            return {'message': "An post with name '{}' already exist." .format(name)}, 400  # if post already exist, return code 400(bad request)

        data = Post.parser.parse_args()
        item = PostModel(name, data['post'])

        try:
            item.save_post_to_db()
        except:
            return {'message': 'An error occured inserting the post.'}, 500 # Internal server error

        return item.json(), 201


class PostList(Resource):   # getting all posts which are exists
    @jwt_required
    def get(self):
        user_activity()
        return {'posts': [post.json() for post in PostModel.query.all()]}

