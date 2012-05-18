from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('twitter_users', meta, autoload=True)
    is_banned = Column('is_banned', Boolean())
    is_banned.create(user)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('twitter_users', meta, autoload=True)
    user.c.is_banned.drop()
