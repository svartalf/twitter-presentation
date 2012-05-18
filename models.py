# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Model = declarative_base()


class User(Model):
    __tablename__ = 'twitter_users'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(30))
    profile_image_url = sqlalchemy.Column(sqlalchemy.String(255))
    is_banned = sqlalchemy.Column(sqlalchemy.Boolean())


class Tweet(Model):
    __tablename__ = 'twitter_tweets'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey('twitter_users.id'))
    text = sqlalchemy.Column(sqlalchemy.Text)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime)

    user = relationship('User', backref=backref('tweets', order_by=id))
