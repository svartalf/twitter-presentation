# -*- coding: utf-8 -*-

import time

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
            # TODO: user cache
            user_exists = db.query(User.id).filter(User.id==tweet.from_user_id).count() > 0
            if not user_exists:
                db.add(User(id=tweet.from_user_id, name=tweet.from_user, profile_image_url=tweet.profile_image_url))
                db.commit()

            if not db.query(Tweet.id).filter(Tweet.id==tweet.id).count():
                db.add(Tweet(id=tweet.id, user_id=tweet.from_user_id, text=tweet.text, created_at=tweet.created_at))
                db.commit()

        time.sleep(5)

if __name__ == '__main__':
    search()