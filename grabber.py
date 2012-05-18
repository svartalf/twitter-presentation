# -*- coding: utf-8 -*-

import json
import time

import zmq
import tweepy
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from models import User, Tweet
import settings

def search():

    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    twitter = tweepy.API(auth)

    engine = create_engine(settings.DATABASE_PATH, convert_unicode=True, echo=settings.DEBUG)
    db = sessionmaker(bind=engine)()

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(settings.ZMQ_PUBLISHER)

    kwargs = {
        'q': ' OR '.join(settings.SEARCH_WORDS),
        'rpp': 10,
    }

    while True:
        latest_id = db.query(Tweet.id).order_by(Tweet.id.desc()).first()
        if latest_id:
            kwargs['since_id'] = latest_id

        try:
            items = list(tweepy.Cursor(twitter.search, **kwargs).items())
        except tweepy.TweepError:
            time.sleep(5)
            continue

        for tweet in items:
            if tweet.text.startswith('RT ') or tweet.to_user_id:
                # Skip retweets and replies
                continue

            # TODO: user cache
            user = db.query(User).get(tweet.from_user_id)
            if not user:
                user = User(id=tweet.from_user_id, name=tweet.from_user, profile_image_url=tweet.profile_image_url, is_banned=False)
                db.add(user)
                db.commit()

            if not db.query(Tweet.id).filter(Tweet.id==tweet.id).count():
                db.add(Tweet(id=tweet.id, user_id=tweet.from_user_id, text=tweet.text, created_at=tweet.created_at))
                db.commit()

                if user.is_banned:
                    continue

                publisher.send('twitter\x00%s' % json.dumps({
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

        time.sleep(5)

if __name__ == '__main__':
    search()
