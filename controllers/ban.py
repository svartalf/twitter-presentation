# -*- coding: utf-8 -*-

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from tornado.web import RequestHandler

import settings
from models import User, Tweet


class BanHandler(RequestHandler):

    def get(self, *args, **kwargs):
        engine = create_engine(settings.DATABASE_PATH, convert_unicode=True, echo=settings.DEBUG)
        db = sessionmaker(bind=engine)()

        queryset = list(db.query(User))
        for user in queryset:
            try:
                user.latest_tweet = db.query(Tweet).filter(Tweet.user_id==user.id).order_by(Tweet.id.desc())[0]
            except IndexError:
                user.latest_tweet = None

        users = sorted([x for x in queryset if not x.is_banned], key=lambda x: x.latest_tweet and x.latest_tweet.created_at)
        banned_users = sorted([x for x in queryset if x.is_banned], key=lambda x: x.latest_tweet and x.latest_tweet.created_at)

        context = {
            'users': users,
            'banned_users': banned_users,
        }

        return self.render('ban.html', **context)

    def post(self, *args, **kwargs):
        user_id = self.get_argument('user_id')
        status = bool(int(self.get_argument('banned')))
        engine = create_engine(settings.DATABASE_PATH, convert_unicode=True, echo=settings.DEBUG)
        db = sessionmaker(bind=engine)()

        user = db.query(User).get(user_id)
        user.is_banned = status

        db.commit()