# -*- coding: utf-8 -*-

import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

STATIC_PATH = os.path.join(PROJECT_ROOT, 'static')

TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'templates')

DATABASE_PATH = 'postgresql://user:password@localhost/twitter'

# Hashtags and keywords for searching
SEARCH_WORDS = ()

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''

try:
    from settings_local import *
except ImportError:
    pass