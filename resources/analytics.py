from datetime import timedelta, datetime
from flask_restful import Resource, reqparse
from flask import request
from db import db
from models.likes import LikeModel
from models.posts import PostModel

class Analytics(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date_from', type=lambda x: datetime.strptime(x,'%Y-%m-%d').date())
    parser.add_argument('date_to', type=lambda x: datetime.strptime(x,'%Y-%m-%d').date())

    def get(self):
        data = Analytics.parser.parse_args()
        date_from = data['date_from']
        date_to = data['date_to']

        all_likes = {}
        posts = {}
        delta = timedelta(days=1)   # for iterate by day
        for post in PostModel.query.all():  # getting all posts
            lists = []
            while date_from <= date_to:
                like_date = {}
                likes = LikeModel.find_by_date(date_from)   # finding likes of each day
                if likes:   # checking if likes exists of each day
                    temp = []
                    for like in likes:
                        if post.id == like.post_id: # finding relation betwen likes and posts
                            temp.append(like.flag)
                
                    like_date[str(date_from)] = sum(temp)   # calculating sum of all likes by day
                    lists.append(like_date) # adding likes by date
                date_from += delta  # iterating on next day

            posts[post.name] = lists    # adding information of likes on each post
            date_from = data['date_from']  # back to original start date for next post

        all_likes['Likes'] = posts

        return all_likes
