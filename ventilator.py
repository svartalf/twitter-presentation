# -*- coding: utf-8 -*-

import zmq

context = zmq.Context()

receiver = context.socket(zmq.PULL)
receiver.bind('tcp://*:14115')

sender = context.socket(zmq.PUB)
sender.bind('tcp://*:14116')

while True:
    message = receiver.recv()
    sender.send(message)
