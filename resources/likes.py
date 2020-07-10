from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, jwt_optional, get_jwt_identity)
from resources.posts import user_activity
from models.posts import PostModel
from models.likes import LikeModel
from models.user import UserModel

class Likes(Resource):
    @jwt_required
    def put(self, name):   # add or remove like from post
        user_activity()

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'messsage': 'Unregistered user. Access denied.'}

        post_check = PostModel.find_by_name(name)
        if post_check is None:  # checking if post exist
            return {'message': "An post with name '{}' not exist." .format(name)}, 400  # if post not exist, return code 400(bad request)
        
        post_id = LikeModel.find_by_post_id(post_check.id)

        if post_id is not None:
            for user_like in post_id:
                if user_like and user_like.user == user.username and user_like.flag == 1:
                    try:
                        user_like.flag = 0
                        user_like.save_like()
                        return {'message': 'Post unliked.'}
                    except:
                        return {'message': 'An error occured liking post.'}, 500 # Internal server error

                elif user_like and user_like.user == user.username and user_like.flag == 0:
                    try:
                        user_like.flag = 1
                        user_like.save_like()
                        return {'message': 'Post liked.'}
                    except:
                        return {'message': 'An error occured liking post.'}, 500 # Internal server error

        try:
            first_like = LikeModel(post_check.id, user.username, 1)
            first_like.save_like()
            return {'message': 'Post liked.'}
        except:
            return {'message': 'An error occured liking post.'}, 500 # Internal server error
