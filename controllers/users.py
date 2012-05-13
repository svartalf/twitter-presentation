# -*- coding: utf-8 -*-

import json

from tornado.web import RequestHandler, HTTPError

from models import User


class ListHandler(RequestHandler):

    def get(self, *args, **kwargs):
        users = self.application.db.query(User)

        self.write(json.dumps([{
                'id': user.id,
                'name': user.name,
                'profile_image_url': user.profile_image_url,
            } for user in users]))

    def post(self, *args, **kwargs):
        print self.request.body

class ReadHandler(RequestHandler):

    def get(self, *args, **kwargs):

        user = self.application.db.query(User).get(kwargs['user_id'])
        if not user:
            raise HTTPError(404)

        self.write({
            'id': user.id,
            'name': user.name,
            'profile_image_url': user.profile_image_url,
        })