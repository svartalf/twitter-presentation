# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, BigInteger, String, Text, DateTime, MetaData, ForeignKey

meta = MetaData()

user = Table('twitter_users', meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(30)),
    Column('profile_image_url', String(255)),
)

tweet = Table('twitter_tweets', meta,
    Column('id', BigInteger, primary_key=True),
    Column('user_id', BigInteger, ForeignKey('twitter_users.id')),
    Column('text', Text),
    Column('created_at', DateTime),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user.create()
    tweet.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    tweet.drop()
    user.drop()