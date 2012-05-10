# -*- coding: utf-8 -*-

from tornado.web import RequestHandler


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        return self.render('index.html')