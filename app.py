# -*- coding: utf-8 -*-

import tornado.web
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sockjs.tornado.router import SockJSRouter
from zmq.eventloop import ioloop

import settings
#import controllers
from controllers import index, websocket

ioloop.install()

websocket = SockJSRouter(websocket.StreamConnection, '/stream')

urlpatterns = [
    (r'^/$', index.IndexHandler),
] + websocket.urls

class Application(tornado.web.Application):

    def __init__(self):

        engine = create_engine(settings.DATABASE_PATH, convert_unicode=True, echo=settings.DEBUG)
        self.db = scoped_session(sessionmaker(bind=engine))

        app_settings = {
            'debug': settings.DEBUG,
            'static_path': settings.STATIC_PATH,
            'template_path': settings.TEMPLATE_PATH,
        }

        super(Application, self).__init__(urlpatterns, **app_settings)

if __name__ == '__main__':
    application = Application()
    application.listen(8888)

    tornado.ioloop.IOLoop.instance().start()
