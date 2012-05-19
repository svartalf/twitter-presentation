# -*- coding: utf-8 -*-

import json

import zmq
from zmq.eventloop.zmqstream import ZMQStream
from sockjs.tornado import SockJSConnection

import settings

class StreamConnection(SockJSConnection):

    def __init__(self, *args, **kwargs):
        super(StreamConnection, self).__init__(*args, **kwargs)

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect('tcp://*:14116')
        socket.setsockopt(zmq.SUBSCRIBE, 'twitter')

        self.stream = ZMQStream(socket)
        self.stream.on_recv(self.incoming)

    def incoming(self, message):
        self.send(json.loads(message[0].split('\x00')[1]))