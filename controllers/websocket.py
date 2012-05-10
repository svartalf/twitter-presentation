# -*- coding: utf-8 -*-

from sockjs.tornado import SockJSConnection

class StreamConnection(SockJSConnection):

    def on_message(self, message):
        self.send(message)
