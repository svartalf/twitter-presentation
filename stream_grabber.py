# -*- coding: utf-8 -*-

import json
import time

import zmq
import tweepy
from tweepy.streaming import StreamListener
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from models import User, Tweet
import settings

class Listener(StreamListener):

    def __init__(self, api):
        super(Listener, self).__init__(api)

        engine = create_engine(settings.DATABASE_PATH, convert_unicode=True, echo=settings.DEBUG)
        self.db = sessionmaker(bind=engine)()

        context = zmq.Context()
        #self.publisher = context.socket(zmq.PUB)
        #self.publisher.bind('tcp://*:14413')

        self.sender = context.socket(zmq.PUSH)
        self.sender.connect('tcp://*:14115')

    def on_status(self, tweet):
        if tweet.text.startswith('RT ') or tweet.to_user_id:
            # Skip retweets and replies
            return

        # TODO: user cache
        user = self.db.query(User).get(tweet.from_user_id)
        if not user:
            user = User(id=tweet.from_user_id, name=tweet.from_user, profile_image_url=tweet.profile_image_url, is_banned=False)
            self.db.add(user)
            self.db.commit()

        if not self.db.query(Tweet.id).filter(Tweet.id==tweet.id).count():
            self.db.add(Tweet(id=tweet.id, user_id=tweet.from_user_id, text=tweet.text, created_at=tweet.created_at))
            self.db.commit()

            if user.is_banned:
                return

            self.sender.send('twitter\x00%s' % json.dumps({
                'class': 'Tweet',
                'action': 'create',
                'data': {
                    'id': tweet.id,
                    'user_id': tweet.from_user_id,
                    'user': {
                        'id': tweet.from_user_id,
                        'name': tweet.from_user,
                        'profile_image_url': tweet.profile_image_url,
                        },
                    'text': tweet.text,
                    'created_at': int(time.mktime(tweet.created_at.timetuple()))*1000,
                    }
            }))

def stream():

    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    twitter = tweepy.API(auth)

    listener = Listener(twitter)

    stream = tweepy.Stream(auth, listener)
    stream.filter(track=settings.SEARCH_WORDS)

if __name__ == '__main__':
    stream()